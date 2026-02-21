// HR Analytics - Employee Cube
// Day 1 Placeholder: Full schema added on Day 4

cube('Employee', {
  sql: `SELECT 1 as id, 'Engineering' as department`,
  measures: {
    count: { type: 'count', title: 'Headcount' }
  },
  dimensions: {
    department: { sql: 'department', type: 'string' }
  }
});
