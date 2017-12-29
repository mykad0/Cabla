const PersonSchema = new Schema({
    uid: Number,
    name: String,
    firstName: String,
    firstNames: Array,
    gender: String, // enum
    parents: Number,
    birth: LifeEvent,
    death: LifeEvent,
    relationships: Number,
    levelOfCertainty: Object // details + enum + default
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
});

const Person = mongoose.model('Person', PersonSchema);