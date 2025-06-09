import express from 'express';

const app = express();

app.use(express.json());

// Basit kullanıcı oluşturma endpointi
app.post('/api/users', (req, res) => {
  const user = {
    id: 1,  // normalde DB'den gelir
    name: req.body.name,
    email: req.body.email,
  };
  res.status(201).json(user);
});

// Middleware, routes, vs.
// örnek:
app.get('/', (_, res) => {
  res.send('Hello World!');
});

export default app;