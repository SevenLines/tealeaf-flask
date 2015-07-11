/**
 * Created by m on 12.07.15.
 */
var Student = Backbone.Model.extend({
    defaults: function () {
        return {
            marks: new MarksCollection()
        }
    }
});
