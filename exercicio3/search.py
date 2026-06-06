from __future__ import annotations

import argparse
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Consulta a collection no ChromaDB e retorna os chunks mais similares."
	)
	parser.add_argument(
		"question",
		type=str,
		help="Pergunta para busca semântica.",
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
		"--top-k",
		type=int,
		default=3,
		help="Quantidade de chunks retornados (padrão: 3).",
	)
	return parser.parse_args()


def cosine_similarity_from_distance(distance: float) -> float:
	"""Converte distância cosseno do ChromaDB em similaridade.

	Para distância cosseno: similarity = 1 - distance.
	"""
	return 1.0 - distance


def main() -> None:
	args = parse_args()

	if args.top_k <= 0:
		raise ValueError("--top-k precisa ser maior que zero.")

	model = SentenceTransformer(args.model)
	question_embedding = model.encode(
		[args.question],
		normalize_embeddings=True,
	)[0]

	client = chromadb.PersistentClient(path=str(args.db_dir))
	collection = client.get_collection(name=args.collection)

	results = collection.query(
		query_embeddings=[question_embedding.tolist()],
		n_results=args.top_k,
		include=["documents", "metadatas", "distances"],
	)

	documents = results.get("documents", [[]])[0]
	metadatas = results.get("metadatas", [[]])[0]
	distances = results.get("distances", [[]])[0]

	if not documents:
		print("Nenhum resultado encontrado na collection.")
		return

	print(f"Pergunta: {args.question}")
	print(f"Collection: {args.collection}")
	print(f"Top-{min(args.top_k, len(documents))} resultados:\n")

	for idx, (doc, metadata, distance) in enumerate(
		zip(documents, metadatas, distances),
		start=1,
	):
		similarity = cosine_similarity_from_distance(float(distance))
		source = metadata.get("source", "desconhecido") if metadata else "desconhecido"
		chunk_index = metadata.get("chunk_index", "?") if metadata else "?"

		print(f"[{idx}] source={source} chunk={chunk_index}")
		print(f"    similarity={similarity:.4f} (distance={float(distance):.4f})")
		print(f"    text={doc}\n")


if __name__ == "__main__":
	main()
