CREATE TABLE IF NOT EXISTS Servidor (
    id_servidor INTEGER PRIMARY KEY,
    nome VARCHAR(70) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    cargo VARCHAR(70) NOT NULL,
    data_ingresso DATE NOT NULL,
    fk_servidor_instituto BIGINT,
    fk_servidor_universidade INTEGER
);

CREATE TABLE IF NOT EXISTS Universidade (
    id_uni INTEGER PRIMARY KEY,
    nome_uni VARCHAR(70) NOT NULL
);

CREATE TABLE IF NOT EXISTS Instituto (
    id_instituto BIGINT PRIMARY KEY,
    nome_instituto VARCHAR(100) NOT NULL,
    fk_instituto_universidade INTEGER
);

CREATE TABLE IF NOT EXISTS Remuneracao (
    id_remuneracao INTEGER PRIMARY KEY AUTO_INCREMENT,
    val_bruto NUMERIC(12,2),
    outras_deducoes NUMERIC(12,2),
    val_ferias NUMERIC(12,2),
    val_natal NUMERIC(12,2),
    val_liquido NUMERIC(12,2),
    fk_remuneracao_servidor INTEGER,
    data DATE
);

CREATE TABLE IF NOT EXISTS Imposto (
    id_imposto INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome_imposto VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS Taxa (
    fk_taxa_remuneracao INTEGER,
    fk_taxa_imposto INTEGER,
    valor NUMERIC(12,2)
);
 
ALTER TABLE Servidor ADD CONSTRAINT FK_Servidor_2
    FOREIGN KEY (fk_servidor_instituto)
    REFERENCES Instituto (id_instituto)
    ON DELETE RESTRICT;
 
ALTER TABLE Servidor ADD CONSTRAINT FK_Servidor_3
    FOREIGN KEY (fk_servidor_universidade)
    REFERENCES Universidade (id_uni)
    ON DELETE CASCADE;
 
ALTER TABLE Remuneracao ADD CONSTRAINT FK_Remuneracao_2
    FOREIGN KEY (fk_remuneracao_servidor)
    REFERENCES Servidor (id_servidor)
    ON DELETE CASCADE;
 
ALTER TABLE Instituto ADD CONSTRAINT FK_Instituto_2
    FOREIGN KEY (fk_instituto_universidade)
    REFERENCES Universidade (id_uni)
    ON DELETE RESTRICT;
 
ALTER TABLE Taxa ADD CONSTRAINT FK_Taxa_1
    FOREIGN KEY (fk_taxa_remuneracao)
    REFERENCES Remuneracao (id_remuneracao)
    ON DELETE SET NULL;
 
ALTER TABLE Taxa ADD CONSTRAINT FK_Taxa_2
    FOREIGN KEY (fk_taxa_imposto)
    REFERENCES Imposto (id_imposto)
    ON DELETE SET NULL;