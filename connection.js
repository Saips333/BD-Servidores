const mysql = require('mysql');
const fs = require('fs');

const fisico = fs.readFileSync('public/fisico.sql').toString();

var created = false;

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  port: 33061,
});

connection.connect((err) => {
  if (err) {
    console.error('❌ Erro na conexão ao SGBD: ' + err.message);
  } else {
    if (created === true) return;
    created = true;
    console.log('Conectado ao SGBD. ✅');
    connection.query('CREATE DATABASE IF NOT EXISTS servidores;', (err, result) => {
      if (err) {
        console.error('❌ Erro ao criar o banco de dados: ' + err.message);
      } else {
        console.log('Banco de dados criado. ✅');
        connection.changeUser({ database: 'servidores' }, (err) => {
          if (err) throw new Error(err);
        });
        createTable();
      }
    });
  }
});

function createTable() {
  const comandos = fisico.split(/(?<=;)/);

  for (const command of comandos) {
    if (command.trim() !== '') {
      connection.query(command, (err, result) => {
        if (err) {
          console.error('❌ Erro ao criar a tabela: ' + err.message);
        }
      });
    }
  }
  console.log('Tabelas criadas. ✅');
}

module.exports = connection;
