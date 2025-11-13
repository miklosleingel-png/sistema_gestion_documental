--
-- PostgreSQL database dump
--

\restrict endl8X5cSzxCa2UVNUSrX2HCMhpKcMzbegTIu61oxItfUnhpz39TmyAgfGqi9Au

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: areas_productoras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.areas_productoras (
    id_area integer NOT NULL,
    unidad_administrativa text,
    area_generadora text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_dependencia integer
);


ALTER TABLE public.areas_productoras OWNER TO postgres;

--
-- Name: areas_productoras_id_area_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.areas_productoras_id_area_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.areas_productoras_id_area_seq OWNER TO postgres;

--
-- Name: areas_productoras_id_area_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.areas_productoras_id_area_seq OWNED BY public.areas_productoras.id_area;


--
-- Name: areas_relacionadas_ext; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.areas_relacionadas_ext (
    id_relacion_ext character varying(10) NOT NULL,
    serie_subserie character varying(50),
    nombre_serie_subserie text,
    area_externa_relacionada text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.areas_relacionadas_ext OWNER TO postgres;

--
-- Name: areas_relacionadas_interno; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.areas_relacionadas_interno (
    id_relacion_interna character varying(10) NOT NULL,
    serie_subserie character varying(50),
    nombre_serie_subserie text,
    area_interna_relacionada text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.areas_relacionadas_interno OWNER TO postgres;

--
-- Name: auditoria_archivistica; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditoria_archivistica (
    id_auditoria integer NOT NULL,
    id_serie integer,
    id_area integer,
    id_funcion integer,
    id_procedimiento integer,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.auditoria_archivistica OWNER TO postgres;

--
-- Name: auditoria_archivistica_id_auditoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auditoria_archivistica_id_auditoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auditoria_archivistica_id_auditoria_seq OWNER TO postgres;

--
-- Name: auditoria_archivistica_id_auditoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auditoria_archivistica_id_auditoria_seq OWNED BY public.auditoria_archivistica.id_auditoria;


--
-- Name: cdd; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cdd (
    id_cdd integer NOT NULL,
    codigo character varying(50) NOT NULL,
    nombre_codigo text,
    tipo_documental character varying(100),
    valor_primario character varying(100),
    valor_secundario character varying(100),
    vigencia_documental character varying(50),
    destino_final character varying(100),
    plazos_conservacion integer,
    fundamento_legal text,
    observaciones text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cdd OWNER TO postgres;

--
-- Name: cdd_id_cdd_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cdd_id_cdd_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cdd_id_cdd_seq OWNER TO postgres;

--
-- Name: cdd_id_cdd_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cdd_id_cdd_seq OWNED BY public.cdd.id_cdd;


--
-- Name: dependencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dependencia (
    id_dependencia integer NOT NULL,
    siglas_dependencia character varying(50) NOT NULL,
    nombre_dependencia text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.dependencia OWNER TO postgres;

--
-- Name: dependencia_id_dependencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dependencia_id_dependencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dependencia_id_dependencia_seq OWNER TO postgres;

--
-- Name: dependencia_id_dependencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dependencia_id_dependencia_seq OWNED BY public.dependencia.id_dependencia;


--
-- Name: funcionarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.funcionarios (
    id_funcionario integer NOT NULL,
    nombre text,
    id_area integer,
    id_dependencia integer,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.funcionarios OWNER TO postgres;

--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.funcionarios_id_funcionario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.funcionarios_id_funcionario_seq OWNER TO postgres;

--
-- Name: funcionarios_id_funcionario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.funcionarios_id_funcionario_seq OWNED BY public.funcionarios.id_funcionario;


--
-- Name: funciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.funciones (
    id_funcion integer NOT NULL,
    funcion text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.funciones OWNER TO postgres;

--
-- Name: funciones_id_funcion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.funciones_id_funcion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.funciones_id_funcion_seq OWNER TO postgres;

--
-- Name: funciones_id_funcion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.funciones_id_funcion_seq OWNED BY public.funciones.id_funcion;


--
-- Name: inventario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventario (
    id_inventario integer NOT NULL,
    clave_cgca character varying(50),
    anio_apertura integer,
    fondo character varying(100),
    unidad_administrativa text,
    area_generadora text,
    numero character varying(50),
    descripcion_expediente text,
    fecha_apertura date,
    fecha_cierre date,
    legajo character varying(50),
    total_legajos integer,
    folios_legajo integer,
    folios_expediente integer,
    archivo character varying(100),
    estanteria character varying(100),
    caja character varying(100),
    id_serie integer,
    id_dependencia integer,
    id_area integer,
    id_cdd integer,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.inventario OWNER TO postgres;

--
-- Name: inventario_expedientes; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.inventario_expedientes AS
 SELECT id_inventario,
    numero,
    clave_cgca,
    anio_apertura,
    fondo,
    unidad_administrativa,
    area_generadora,
    descripcion_expediente,
    fecha_apertura,
    fecha_cierre,
    legajo,
    total_legajos,
    folios_legajo,
    folios_expediente,
    archivo,
    estanteria,
    caja,
    id_serie,
    id_dependencia,
    id_area,
    id_cdd,
    registrado_por,
    fecha_registro,
    fecha_modificacion
   FROM public.inventario;


ALTER VIEW public.inventario_expedientes OWNER TO postgres;

--
-- Name: inventario_id_inventario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.inventario_id_inventario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inventario_id_inventario_seq OWNER TO postgres;

--
-- Name: inventario_id_inventario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.inventario_id_inventario_seq OWNED BY public.inventario.id_inventario;


--
-- Name: procedimientos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.procedimientos (
    id_procedimiento integer NOT NULL,
    procedimiento text,
    clave_procedimiento character varying(50),
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.procedimientos OWNER TO postgres;

--
-- Name: procedimientos_id_procedimiento_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.procedimientos_id_procedimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.procedimientos_id_procedimiento_seq OWNER TO postgres;

--
-- Name: procedimientos_id_procedimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.procedimientos_id_procedimiento_seq OWNED BY public.procedimientos.id_procedimiento;


--
-- Name: series_documentales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.series_documentales (
    id_serie integer NOT NULL,
    codigo character varying(50) NOT NULL,
    nombre_codigo text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.series_documentales OWNER TO postgres;

--
-- Name: series_documentales_id_serie_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.series_documentales_id_serie_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.series_documentales_id_serie_seq OWNER TO postgres;

--
-- Name: series_documentales_id_serie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.series_documentales_id_serie_seq OWNED BY public.series_documentales.id_serie;


--
-- Name: transparencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transparencia (
    id_transparencia character varying(10) NOT NULL,
    codigo_serie character varying(50),
    tradicion_original text,
    tradicion_copia text,
    soporte_papel text,
    soporte_digital text,
    condiciones_acceso text,
    fundamento_legal text,
    registrado_por character varying(100),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.transparencia OWNER TO postgres;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre_usuario character varying(100) NOT NULL,
    "contraseña_hash" text NOT NULL,
    rol character varying(50),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    unidad_admin character varying(100)
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- Name: areas_productoras id_area; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.areas_productoras ALTER COLUMN id_area SET DEFAULT nextval('public.areas_productoras_id_area_seq'::regclass);


--
-- Name: auditoria_archivistica id_auditoria; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_archivistica ALTER COLUMN id_auditoria SET DEFAULT nextval('public.auditoria_archivistica_id_auditoria_seq'::regclass);


--
-- Name: cdd id_cdd; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cdd ALTER COLUMN id_cdd SET DEFAULT nextval('public.cdd_id_cdd_seq'::regclass);


--
-- Name: dependencia id_dependencia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dependencia ALTER COLUMN id_dependencia SET DEFAULT nextval('public.dependencia_id_dependencia_seq'::regclass);


--
-- Name: funcionarios id_funcionario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funcionarios ALTER COLUMN id_funcionario SET DEFAULT nextval('public.funcionarios_id_funcionario_seq'::regclass);


--
-- Name: funciones id_funcion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funciones ALTER COLUMN id_funcion SET DEFAULT nextval('public.funciones_id_funcion_seq'::regclass);


--
-- Name: inventario id_inventario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventario ALTER COLUMN id_inventario SET DEFAULT nextval('public.inventario_id_inventario_seq'::regclass);


--
-- Name: procedimientos id_procedimiento; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.procedimientos ALTER COLUMN id_procedimiento SET DEFAULT nextval('public.procedimientos_id_procedimiento_seq'::regclass);


--
-- Name: series_documentales id_serie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.series_documentales ALTER COLUMN id_serie SET DEFAULT nextval('public.series_documentales_id_serie_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- Name: areas_productoras areas_productoras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.areas_productoras
    ADD CONSTRAINT areas_productoras_pkey PRIMARY KEY (id_area);


--
-- Name: areas_relacionadas_ext areas_relacionadas_ext_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.areas_relacionadas_ext
    ADD CONSTRAINT areas_relacionadas_ext_pkey PRIMARY KEY (id_relacion_ext);


--
-- Name: areas_relacionadas_interno areas_relacionadas_interno_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.areas_relacionadas_interno
    ADD CONSTRAINT areas_relacionadas_interno_pkey PRIMARY KEY (id_relacion_interna);


--
-- Name: auditoria_archivistica auditoria_archivistica_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_archivistica
    ADD CONSTRAINT auditoria_archivistica_pkey PRIMARY KEY (id_auditoria);


--
-- Name: cdd cdd_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cdd
    ADD CONSTRAINT cdd_codigo_key UNIQUE (codigo);


--
-- Name: cdd cdd_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cdd
    ADD CONSTRAINT cdd_pkey PRIMARY KEY (id_cdd);


--
-- Name: dependencia dependencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dependencia
    ADD CONSTRAINT dependencia_pkey PRIMARY KEY (id_dependencia);


--
-- Name: dependencia dependencia_siglas_dependencia_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dependencia
    ADD CONSTRAINT dependencia_siglas_dependencia_key UNIQUE (siglas_dependencia);


--
-- Name: funcionarios funcionarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_pkey PRIMARY KEY (id_funcionario);


--
-- Name: funciones funciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funciones
    ADD CONSTRAINT funciones_pkey PRIMARY KEY (id_funcion);


--
-- Name: inventario inventario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_pkey PRIMARY KEY (id_inventario);


--
-- Name: procedimientos procedimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.procedimientos
    ADD CONSTRAINT procedimientos_pkey PRIMARY KEY (id_procedimiento);


--
-- Name: series_documentales series_documentales_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.series_documentales
    ADD CONSTRAINT series_documentales_codigo_key UNIQUE (codigo);


--
-- Name: series_documentales series_documentales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.series_documentales
    ADD CONSTRAINT series_documentales_pkey PRIMARY KEY (id_serie);


--
-- Name: transparencia transparencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transparencia
    ADD CONSTRAINT transparencia_pkey PRIMARY KEY (id_transparencia);


--
-- Name: usuarios usuarios_nombre_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_nombre_usuario_key UNIQUE (nombre_usuario);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: auditoria_archivistica auditoria_archivistica_id_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_archivistica
    ADD CONSTRAINT auditoria_archivistica_id_area_fkey FOREIGN KEY (id_area) REFERENCES public.areas_productoras(id_area);


--
-- Name: auditoria_archivistica auditoria_archivistica_id_funcion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_archivistica
    ADD CONSTRAINT auditoria_archivistica_id_funcion_fkey FOREIGN KEY (id_funcion) REFERENCES public.funciones(id_funcion);


--
-- Name: auditoria_archivistica auditoria_archivistica_id_procedimiento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_archivistica
    ADD CONSTRAINT auditoria_archivistica_id_procedimiento_fkey FOREIGN KEY (id_procedimiento) REFERENCES public.procedimientos(id_procedimiento);


--
-- Name: auditoria_archivistica auditoria_archivistica_id_serie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria_archivistica
    ADD CONSTRAINT auditoria_archivistica_id_serie_fkey FOREIGN KEY (id_serie) REFERENCES public.series_documentales(id_serie);


--
-- Name: funcionarios funcionarios_id_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_id_area_fkey FOREIGN KEY (id_area) REFERENCES public.areas_productoras(id_area);


--
-- Name: funcionarios funcionarios_id_dependencia_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funcionarios
    ADD CONSTRAINT funcionarios_id_dependencia_fkey FOREIGN KEY (id_dependencia) REFERENCES public.dependencia(id_dependencia);


--
-- Name: inventario inventario_id_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_id_area_fkey FOREIGN KEY (id_area) REFERENCES public.areas_productoras(id_area);


--
-- Name: inventario inventario_id_cdd_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_id_cdd_fkey FOREIGN KEY (id_cdd) REFERENCES public.cdd(id_cdd);


--
-- Name: inventario inventario_id_dependencia_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_id_dependencia_fkey FOREIGN KEY (id_dependencia) REFERENCES public.dependencia(id_dependencia);


--
-- Name: inventario inventario_id_serie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_id_serie_fkey FOREIGN KEY (id_serie) REFERENCES public.series_documentales(id_serie);


--
-- PostgreSQL database dump complete
--

\unrestrict endl8X5cSzxCa2UVNUSrX2HCMhpKcMzbegTIu61oxItfUnhpz39TmyAgfGqi9Au

