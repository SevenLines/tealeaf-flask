var TaskItem = Backbone.Model.extend({

});

var TaskItemView = Backbone.View.extend({
    initialize: function(model, options) {
        this.editor = null;
        _.bindAll(this, "render");
        this.render();
        // this.editor = this.$el.find(".m-task-description span").summernote();
    },
    events: {
        "click .m-task-btn-save": "save"
    },

    render: function () {
        this.$el.find('.m-task-btn-save').toggle(this.editor !== null);
    },

    removeEditor: function () {
        if (this.editor) {
            this.$el.find('.m-task-description').summernote('destroy');
            this.editor = null;
            this.render();
        }
    },

    createEditor: function () {
        this.editor = this.$el.find('.m-task-description').summernote();
        this.render();
    },

    save: function () {
        var self = this;
        $.ajax({
            type: "POST",
            contentType: 'application/json',
            url: '/task/' + this.$el.data('id') + '/',
            data: JSON.stringify({
                'description': this.editor.summernote('code')
            })
        }).done(function () {
            new Noty({
                theme: 'relax',
                text: "Сохранено",
                type: 'success',
                timeout: 1000
            }).show();
            self.removeEditor()
        }).fail(function () {
            new Noty({
                theme: 'relax',
                text: "Ошибка при сохранении",
                type: 'error',
                timeout: 1000
            }).show();
        })
    }
});