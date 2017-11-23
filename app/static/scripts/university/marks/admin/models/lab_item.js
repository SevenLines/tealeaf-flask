var LabItem = Backbone.Model.extend({
    save: function () {
        $.ajax({
            url: '/lab/' + this.get('id') + '/',
            data: JSON.stringify(this.toJSON()),
            method: "POST",
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        })
    },

    toJSON: function () {
        return {
            id: this.get('id'),
            title: this.get('title'),
            description: this.get('description'),
            discipline_id: this.get('discipline_id'),
            visible: this.get('visible'),
            regular: this.get('regular'),
            order: this.get('order')
        }
    }
});


var LabItemView = Backbone.View.extend({
    initialize: function () {
        _.bindAll(this, "render");
        this.model.on('change', this.render);
        this.render()
    },

    events: {
        "click .toggle-hide": "toggleHide"
    },

    toggleHide: function (e) {
        this.model.set('visible', !this.model.get("visible"));
        this.model.save();
        e.stopPropagation();
        return false
    },

    render: function () {
        var is_visible = this.model.get("visible");
        this.$el.find(".toggle-hide ").toggleClass("btn-default", !is_visible);
        this.$el.find(".toggle-hide ").toggleClass("btn-success", is_visible);
        this.$el.find(".toggle-hide .fa").toggleClass("fa-eye-slash", !is_visible);
        this.$el.find(".toggle-hide .fa").toggleClass("fa-eye", is_visible)
    }
});