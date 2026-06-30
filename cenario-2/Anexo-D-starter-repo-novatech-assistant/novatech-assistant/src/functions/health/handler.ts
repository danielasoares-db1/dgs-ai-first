import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { logger } from "../../shared/logger";

type HealthResponseBody = {
	status: "ok";
	service: "novatech-assistant";
};

export async function healthHandler(
	request: HttpRequest,
	context: InvocationContext,
): Promise<HttpResponseInit> {
	if (request.method !== "GET") {
		logger.warn({ method: request.method }, "Rejected request with unsupported method");

		return {
			status: 405,
			jsonBody: {
				error: "Method not allowed",
				details: ["Only GET is supported for this endpoint"],
			},
		};
	}

	logger.info({ invocationId: context.invocationId }, "Health check succeeded");

	const body: HealthResponseBody = {
		status: "ok",
		service: "novatech-assistant",
	};

	return {
		status: 200,
		jsonBody: body,
	};
}

app.http("health", {
	methods: ["GET"],
	authLevel: "anonymous",
	route: "health",
	handler: healthHandler,
});
