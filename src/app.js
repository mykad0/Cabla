app.use((req, res, next) => {
    const err = new Error('This endpoint does not exists');
    err.status = 404;
    next(err);
});

app.use((err, req, res, next) => {
    res.status(err.status || 500);
    res.json({error: err.message});
});

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header(
        'Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Accept'
    );

    if (req.method === 'Options') {
        res.header('Access-Control-Allow-Methods', 'GET', 'PUT, POST, DELETE');
        return res.status(200).json({});
    }
});