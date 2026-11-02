Udatracker Order Tracking Service
I kept the OrderTracker business logic independent of Flask so it could be tested in isolation and reused without depending on the web framework.
TDD helped me work incrementally. Failing tests exposed issues such as missing return values, duplicate order handling, incorrect filtering and indentation errors. Running one focused test at a time made debugging more manageable.
I used copies of stored order dictionaries when updating status to avoid unintentionally modifying the original data.
If I continued the project, I would replace the in-memory store with persistent database storage and add stricter request validation and more API error-path tests.