// Mirrors backend `course_service.code_key`: 'CS-351', 'cs351' and 'CS 351'
// are the same course code. The server's duplicate check is authoritative;
// this only lets the form catch an obvious duplicate before submitting.
export const codeKey = (code) => code.toLowerCase().replace(/[^a-z0-9]/g, '')
