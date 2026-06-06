from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import chromadb
from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
	"""Representa um trecho de texto pronto para indexação."""

	chunk_id: str
	source_file: str
	chunk_index: int
	text: str


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Lê markdown, gera embeddings e salva chunks no ChromaDB."
	)
	parser.add_argument(
		"--docs-dir",
		type=Path,
		default=Path("documentos"),
		help="Diretório com arquivos .md (padrão: documentos).",
	)
	parser.add_argument(
		"--db-dir",
		type=Path,
		default=Path("chroma_db"),
		help="Diretório de persistência do ChromaDB (padrão: chroma_db).",
	)
	parser.add_argument(
		"--collection",
		type=str,
		default="novatech_docs",
		help="Nome da collection no ChromaDB.",
	)
	parser.add_argument(
		"--model",
		type=str,
		default="sentence-transformers/all-MiniLM-L6-v2",
		help="Modelo sentence-transformers para embeddings.",
	)
	parser.add_argument(
		"--chunk-size",
		type=int,
		default=700,
		help="Tamanho alvo do chunk em caracteres.",
	)
	parser.add_argument(
		"--chunk-overlap",
		type=int,
		default=120,
		help="Sobreposição em caracteres entre chunks consecutivos.",
	)
	parser.add_argument(
		"--reset",
		action="store_true",
		help="Apaga a collection antes de indexar novamente.",
	)
	return parser.parse_args()


def read_markdown_files(docs_dir: Path) -> list[tuple[Path, str]]:
	if not docs_dir.exists():
		raise FileNotFoundError(f"Diretório não encontrado: {docs_dir}")

	files = sorted(docs_dir.rglob("*.md"))
	if not files:
		raise FileNotFoundError(f"Nenhum arquivo .md encontrado em: {docs_dir}")

	data: list[tuple[Path, str]] = []
	for file_path in files:
		text = file_path.read_text(encoding="utf-8").strip()
		if text:
			data.append((file_path, text))
	return data


def sliding_window_chunks(text: str, chunk_size: int, chunk_overlap: int) -> Iterable[str]:
	if chunk_size <= 0:
		raise ValueError("chunk_size precisa ser > 0")
	if chunk_overlap < 0:
		raise ValueError("chunk_overlap precisa ser >= 0")
	if chunk_overlap >= chunk_size:
		raise ValueError("chunk_overlap precisa ser menor que chunk_size")

	normalized = " ".join(text.split())
	start = 0
	while start < len(normalized):
		end = min(len(normalized), start + chunk_size)
		yield normalized[start:end]
		if end == len(normalized):
			break
		start = end - chunk_overlap


def build_chunks(
	files_with_text: list[tuple[Path, str]],
	docs_dir: Path,
	chunk_size: int,
	chunk_overlap: int,
) -> List[Chunk]:
	chunks: List[Chunk] = []
	for path, text in files_with_text:
		rel_source = str(path.relative_to(docs_dir))
		for chunk_idx, chunk_text in enumerate(
			sliding_window_chunks(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
		):
			raw_key = f"{rel_source}:{chunk_idx}:{chunk_text}"
			stable_id = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:24]
			chunks.append(
				Chunk(
					chunk_id=stable_id,
					source_file=rel_source,
					chunk_index=chunk_idx,
					text=chunk_text,
				)
			)
	return chunks


def reset_collection_if_requested(
	client: chromadb.ClientAPI, collection_name: str, reset: bool
) -> None:
	if not reset:
		return
	try:
		client.delete_collection(name=collection_name)
		print(f"Collection '{collection_name}' apagada (--reset).")
	except Exception:
		# Se não existir ainda, seguimos sem erro.
		pass


def main() -> None:
	args = parse_args()

	files_with_text = read_markdown_files(args.docs_dir)
	chunks = build_chunks(
		files_with_text,
		docs_dir=args.docs_dir,
		chunk_size=args.chunk_size,
		chunk_overlap=args.chunk_overlap,
	)

	if not chunks:
		raise RuntimeError("Não foi possível gerar chunks a partir dos arquivos markdown.")

	print(f"Arquivos lidos: {len(files_with_text)}")
	print(f"Chunks gerados: {len(chunks)}")
	print(f"Modelo de embedding: {args.model}")

	model = SentenceTransformer(args.model)
	texts = [chunk.text for chunk in chunks]
	embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

	client = chromadb.PersistentClient(path=str(args.db_dir))
	reset_collection_if_requested(client, args.collection, args.reset)

	collection = client.get_or_create_collection(name=args.collection)
	collection.upsert(
		ids=[chunk.chunk_id for chunk in chunks],
		documents=texts,
		embeddings=embeddings.tolist(),
		metadatas=[
			{
				"source": chunk.source_file,
				"chunk_index": chunk.chunk_index,
			}
			for chunk in chunks
		],
	)

	print(
		f"Indexação concluída. Collection '{args.collection}' contém {collection.count()} registros."
	)


if __name__ == "__main__":
	main()
