const RelationshipSchema = new Schema({
    uid: Number,
    partners: Array,
    marriage: LifeEvent,
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
});

const Relationship = mongoose.model('Relationship', RelationshipSchema);
