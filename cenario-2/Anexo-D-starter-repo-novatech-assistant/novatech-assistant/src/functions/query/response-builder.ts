import { HttpResponseInit } from "@azure/functions";

type ErrorDetail = Record<string, unknown> | string;

export function buildBadRequestResponse(details: ErrorDetail | ErrorDetail[]): HttpResponseInit {
	return {
		status: 400,
		jsonBody: {
			error: "Invalid request payload",
			details,
		},
	};
}

export function buildMethodNotAllowedResponse(): HttpResponseInit {
	return {
		status: 405,
		jsonBody: {
			error: "Method not allowed",
			details: ["Only POST is supported for this endpoint"],
		},
	};
}

export function buildAcceptedResponse(): HttpResponseInit {
	return {
		status: 202,
		jsonBody: {
			message: "Query accepted for processing",
			source_document: null,
		},
	};
}
