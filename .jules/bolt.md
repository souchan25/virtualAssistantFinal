
## 2024-03-01 - N+1 Query in student_directory API
**Learning:** Found an N+1 query bottleneck in `student_directory` view when constructing the frontend `students_data` list. It triggers multiple DB queries per student in the loop to calculate `recent_symptoms`, `active_meds`, `med_logs` for adherence, and `pending_followups`. For 5 students it made 75 queries, and for 15 students it made 215 queries. This scales poorly with PageNumberPagination (20 students per page = ~285 queries).
**Action:** Optimize `student_directory` view to use `Prefetch` combined with annotations or pre-fetch all needed related objects efficiently, minimizing queries inside the loop.
