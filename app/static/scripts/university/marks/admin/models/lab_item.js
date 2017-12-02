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

    increaseOrder: function () {
    },

    decreaseOrder: function () {
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
    initialize: function (model, options) {
        _.bindAll(this, "render");
        this.lessonEditor = options.lessonEditor;
        this.model.on('change', this.render);
        this.render()
    },

    events: {
        "click .toggle-hide": "toggleHide",
        "click .btn-order-up": "orderUp",
        "click .btn-order-down": "orderDown",
        "click .btn-save": "save",
        "click input": "stop",
        "keyup .lab-title-input": "setTitle",
    },

    save: function (e) {
        this.model.save();
        e.stopPropagation();
    },

    stop: function (e) {
        e.stopPropagation();
    },

    setTitle: function (e) {
        console.log(e)
        this.model.set("title", e.currentTarget.value)
    },

    toggleHide: function (e) {
        this.model.set('visible', !this.model.get("visible"));
        this.model.save();
        e.stopPropagation();
    },

    orderUp: function (e) {
        this.model.increaseOrder();
        e.stopPropagation();
    },

    orderDown: function (e) {
        this.model.decreaseOrder();
        e.stopPropagation();
    },

    render: function () {
        var is_visible = this.model.get("visible");
        this.$el.find(".toggle-hide ").toggleClass("btn-default", !is_visible);
        this.$el.find(".toggle-hide ").toggleClass("btn-success", is_visible);
        this.$el.find(".toggle-hide .fa").toggleClass("fa-eye-slash", !is_visible);
        this.$el.find(".toggle-hide .fa").toggleClass("fa-eye", is_visible);
    }
});