import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { logger } from "../../shared/logger";
import {
  buildAcceptedResponse,
  buildBadRequestResponse,
  buildMethodNotAllowedResponse,
} from "./response-builder";
import { mapZodIssues, validateQueryRequest } from "./validator";

export async function queryHandler(
  request: HttpRequest,
  context: InvocationContext,
): Promise<HttpResponseInit> {
  if (request.method !== "POST") {
    logger.warn({ method: request.method }, "Rejected request with unsupported method");
    return buildMethodNotAllowedResponse();
  }

  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    logger.warn("Rejected request with malformed JSON body");
    return buildBadRequestResponse(["Request body must be valid JSON"]);
  }

  const validation = validateQueryRequest(payload);
  if (!validation.success) {
    const details = mapZodIssues(validation.error.issues);
    logger.warn({ details }, "Rejected request with invalid payload");
    return buildBadRequestResponse(details);
  }

  logger.info({ invocationId: context.invocationId }, "Query accepted for processing");
  return buildAcceptedResponse();
}

app.http("query", {
  methods: ["POST"],
  authLevel: "anonymous",
  route: "query",
  handler: queryHandler,
});
