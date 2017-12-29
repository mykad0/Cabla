relationshipRouter.get('/relationships', (req, res) => {
    Relationship.find({}).exec((err, relationships) => {
        if (err) return next(err);
        res.json(relationships);
    });
});

relationshipRouter.get('/relationships/:relationshipId', (req, res) => {
    Relationship.find({uid: relationshipId}).exec((err, relationship) => {
        if (err) return next(err);
        res.json(relationship);
    });
});

relationshipRouter.post('/relationships/:relationshipId', (req, res) => {
  const relationship = new Relationship(req.body);
    Relationship.save((err, relationship) => {
        if (err) return next(err);
        res.json(relationship);
    });
});

relationshipRouter.put('/relationships/:relationshipId', (req, res) => {
    Relationship.find({uid: relationshipId}).update((req.body, (err, relationship) => {
        if (err) return next(err);
        res.json(relationship);
    });
});

relationshipRouter.delete('/relationships/:relationshipId', (req, res) => {
    Relationship.find({uid: relationshipId}).remove((req.body, (err, relationship) => {
        if (err) return next(err);
        res.json(success: 'Relationship ' + relationshipId + 'has been removed');
    });
});