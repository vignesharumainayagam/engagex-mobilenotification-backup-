
from __future__ import unicode_literals
import frappe


def get_context(context):

	user = frappe.session.user
	ExamId=frappe.form_dict.Exam

	result = frappe.get_list("Exam Result", fields=["user", "student", "exam_id", "exam_start_date", "exam_end_date", "name",
													"attended", "correct_answers", "wrong_answers", "total_marks", "secured__marks"],
													filters={"user": user, "exam_id": ExamId}, limit_page_length= 500, )
	for x in result:
		x.answers = frappe.get_list("User Answer", fields=["question_id", "question", "correct_answer", "user_answer", "is_user_answer_correct", "question_id"],
												   filters={"parent": x.name, "parenttype": "Exam Result"}, limit_page_length= 500, )

	for y in x.answers:
		y.options = frappe.get_list("Answers", fields=["options", "is_correct"],
												   filters={"parent": y.question_id}, limit_page_length= 500, )
		

	context.result = result
	context.user = user
	context.exam_id = ExamId
