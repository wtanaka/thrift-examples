namespace py typecheck

struct Point {
  1: required double x;
  2: required double y;
}

struct Review {
  1: required i32 rating;
  2: optional string text;
}

struct Place {
  1: required string name;
  2: required Point location;
  3: optional Review review;
}

