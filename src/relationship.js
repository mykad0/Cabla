const RelationshipSchema = new Schema({
    uid: Number,
    partners: Array,
    marriage: LifeEvent,
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
    certainty: Object // details + enum + default
});

RelationshipSchema.method('insert', function (doc, callback) {
  Object.assign(this, doc, { createdAt: new Date() });
  this.parent().save(callback);
});

RelationshipSchema.method('update', function (updates, callback) {
  Object.assign(this, updates, { updatedAt: new Date() });
  this.parent().save(callback);
});

const Relationship = mongoose.model('Relationship', RelationshipSchema);
