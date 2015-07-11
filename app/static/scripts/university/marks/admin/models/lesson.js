/**
 * Created by m on 12.07.15.
 */
var Lesson = Backbone.Model.extend({
    defaults: function () {
        return {
            marks: new MarksCollection()
        }
    }
});
