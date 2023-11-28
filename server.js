const express = require('express');
const app = express();
const port = 3000;

// Configurar a view engine EJS
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

// Rotas
const router = require('./routes/consultas');
app.use('/', router);
app.use(express.static(__dirname + '/public'));

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
