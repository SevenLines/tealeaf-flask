var TaskItem = Backbone.Model.extend({

});

var TaskItemView = Backbone.View.extend({
    initialize: function(model, options) {
        this.editor = null;
        this.complexity = this.$el.data('complexity');
        this.ignore = this.$el.data('ignore') === 'True';
        _.bindAll(this, "render");
        this.render();
    },
    events: {
        "click .m-task-btn-save": "save",
        "click .m-task-btn-close": "close",
        "click .m-task-btn-ignore": "toggleIgnore",
        "click .m-task-btn-actions .difficult div": 'setDifficult'
    },

    render: function () {
        var self = this;
        // ignore class
        this.$el.find('.m-task-btn-ignore').removeClass("btn-default btn-success");
        this.$el.find('.m-task-btn-ignore').addClass(this.ignore ? "btn-default" : 'btn-success');

        this.$el.find('.m-task-btn-actions').toggle(this.editor !== null);
        this.$el.find('.m-task-btn-actions .difficult div').removeClass("active");
        this.$el.find('.m-task-btn-actions .difficult div[data-id="' + self.complexity + '"]').addClass("active");
        this.$el.removeClass("easy medium hard nightmare");
        this.$el.addClass(["", "easy", 'medium', 'hard', 'nightmare'][self.complexity]);
    },

    setDifficult: function (e) {
        this.complexity = $(e.currentTarget).data('id');
        this.render()
    },

    toggleIgnore: function (e) {
        this.ignore = !this.ignore;
        this.save();
        this.render()
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

    close: function () {
        this.removeEditor()
    },

    save: function () {
        var self = this;
        $.ajax({
            type: "POST",
            contentType: 'application/json',
            url: '/task/' + this.$el.data('id') + '/',
            data: JSON.stringify({
                'description': this.editor.summernote('code'),
                'complexity': this.complexity,
                'ignore': this.ignore,
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