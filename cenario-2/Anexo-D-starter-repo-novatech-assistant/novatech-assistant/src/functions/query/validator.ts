import { z } from "zod";

export const queryRequestSchema = z.object({
	question: z
		.string({ required_error: "question is required" })
		.trim()
		.min(1, "question must be a non-empty string"),
});

export type QueryRequest = z.infer<typeof queryRequestSchema>;

export function validateQueryRequest(payload: unknown) {
	return queryRequestSchema.safeParse(payload);
}

export function mapZodIssues(issues: z.ZodIssue[]) {
	return issues.map((issue) => ({
		path: issue.path.join("."),
		message: issue.message,
		code: issue.code,
	}));
}
