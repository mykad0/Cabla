const PersonSchema = new Schema({
    uid: Number,
    name: String,
    firstName: String,
    firstNames: Array,
    gender: String, // enum
    parentRelationship: Number,
    birth: LifeEvent,
    death: LifeEvent,
    relationships: Number,
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
    certainty: Object // details + enum + default
});

PersonSchema.method('insert', function (doc, callback) {
  Object.assign(this, doc, { createdAt: new Date() });
  this.parent().save(callback);
});

PersonSchema.method('update', function (updates, callback) {
  Object.assign(this, updates, { updatedAt: new Date() });
  this.parent().save(callback);
});

const Person = mongoose.model('Person', PersonSchema);