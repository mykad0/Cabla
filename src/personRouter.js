personRouter.get('/persons', (req, res) => {
    Person.find({}).exec((err, persons) => {
        if (err) return next(err);
        res.json(persons);
    });
});

personRouter.get('/persons/:personId', (req, res) => {
    Person.find({uid: personId}).exec((err, person) => {
        if (err) return next(err);
        res.json(person);
    });
});

personRouter.post('/persons/:personId', (req, res) => {
    const person = new Person(req.body);
    Person.save((err, person) => {
        if (err) return next(err);
        res.json(person);
    });
});

personRouter.put('/persons/:personId', (req, res) => {
    Person.find({uid: personId}).update((req.body, (err, person) => {
        if (err) return next(err);
        res.json(person);
    });
});

personRouter.delete('/persons/:personId', (req, res) => {
    Person.find({uid: personId}).remove((req.body, (err, person) => {
        if (err) return next(err);
        res.json(success: 'Person ' + personId + 'has been removed');
    });
});