CREATE TABLE arbol (
    id_arbol        int NOT NULL,
    id_especie      int NOT NULL,
    id_ubicacion    int NOT NULL,
    id_follaje      int NOT NULL,
    long            numeric,
    lat             numeric,
    coord_x         numeric,
    coord_y         numeric,
    inclinacion     int,
    diametro        int,
    altura_total    int,
    CONSTRAINT pk_arbol PRIMARY KEY(id_arbol)
);


CREATE TABLE especie (
    id_especie      int NOT NULL,
    nombre_comun    char(100),
    nombre_cientifico  char(100),
    id_genero       int NOT NULL,
    id_origen       int NOT NULL,
    CONSTRAINT pk_especie PRIMARY KEY(id_especie)
);


CREATE TABLE  genero (
    id_genero       int NOT NULL,
    nombre_genero   char(30),
    id_familia      int,
    CONSTRAINT pk_genero PRIMARY KEY(id_genero)
);


CREATE TABLE  familia (
    id_familia      int NOT NULL,
    nombre_familia  char(30),
    CONSTRAINT pk_familia PRIMARY KEY(id_familia)
);


CREATE TABLE  origen (
    id_origen       int NOT NULL,
    origen          char(100),
    CONSTRAINT pk_origen PRIMARY KEY(id_origen)
);


CREATE TABLE  follaje(
    id_follaje      int NOT NULL,
    tipo_follaje    char(50),
    CONSTRAINT pk_follaje PRIMARY KEY(id_follaje)
);


CREATE TABLE ubicacion(
    id_ubicacion    int NOT NULL,
    espacio_verde   char(500),
    ubicacion       char(500),
    CONSTRAINT pk_ubicacion PRIMARY KEY(id_ubicacion)
);

--arbol - especie
ALTER TABLE arbol ADD CONSTRAINT fk_arbol_especie FOREIGN KEY (id_especie) REFERENCES especie (id_especie) ON UPDATE CASCADE;
--arbol - ubicacion
ALTER TABLE arbol ADD CONSTRAINT fk_arbol_ubicacion FOREIGN KEY (id_ubicacion) REFERENCES ubicacion (id_ubicacion) ON UPDATE CASCADE;
--arbol - follaje
ALTER TABLE arbol ADD CONSTRAINT fk_arbol_follaje FOREIGN KEY (id_follaje) REFERENCES follaje (id_follaje) ON UPDATE CASCADE;

--especie - genero
ALTER TABLE especie ADD CONSTRAINT fk_especie_genero FOREIGN KEY (id_genero) REFERENCES genero (id_genero) ON UPDATE CASCADE;

--genero - familia
ALTER TABLE genero ADD CONSTRAINT fk_genero_familia FOREIGN KEY (id_familia) REFERENCES familia (id_familia) ON UPDATE CASCADE;

--especie - origen
ALTER TABLE especie ADD CONSTRAINT fk_especie_origen FOREIGN KEY (id_origen) REFERENCES origen (id_origen) ON UPDATE CASCADE;