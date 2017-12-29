const LifeEventSchema = new Schema({
    place: String,
    date: Date,
    docs: Array,
    note: String
});

const CheckableInfoSchema = new Schema({
	// anything
    levelOfCertainty: String // enum
});

const LifeEvent = mongoose.model('LifeEvent', LifeEventSchema);
const CheckableInfo = mongoose.model('CheckableInfo', CheckableInfoSchema);