CREATE TABLE news(
  titulo text, 
  cuerpo text, 
  fecha_publicacion int, 
  diario text, 
  url text,
  page int
);

CREATE TABLE classified_news(
  titulo text, 
  cuerpo text, 
  diario text, 
  url text,
  category text
);