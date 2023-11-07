const express = require('express');
const app = express();
const port = 3000;

// Configurar a view engine EJS
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

// Rotas
const professoresRouter = require('./routes/professores');
app.use('/professores', professoresRouter);

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
