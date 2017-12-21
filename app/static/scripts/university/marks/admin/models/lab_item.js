var LabItem = Backbone.Model.extend({
    save: function () {
        return $.ajax({
            url: '/lab/' + this.get('id') + '/',
            data: JSON.stringify(this.toJSON()),
            method: "POST",
            contentType: "application/json; charset=utf-8",
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
        var self = this;
        this.lessonEditor = options.lessonEditor;
        this.model.on('change', this.render);
        this.taskOrder = [];

        this.$el.find('.m-task').each(function (index, item) {
            item.view = new TaskItemView({
                el: item
            })
        });
        this.sortable = Sortable.create(this.$el.find('.m-lab-info-tasks')[0], {
            handle: '.m-task-label',
            onEnd: function () {
                self.taskOrder = [];
                self.$el.find('.m-task').each(function (index, item) {
                    self.taskOrder.push($(item).data('id'));
                    $(item).find('.m-task-label').html(index + 1);
                });
                $.ajax({
                    url: '/lab/set-tasks-order/',
                    type: "POST",
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'order': self.taskOrder
                    })
                }).done(function () {
                    new Noty({
                        theme: 'relax',
                        text: "Сохранено",
                        type: 'success',
                        timeout: 1000
                    }).show();
                }).fail(function () {
                    new Noty({
                        theme: 'relax',
                        text: "Ну удалось отсортировать",
                        type: 'error',
                        timeout: 1000
                    }).show();
                })
            },
        });

        this.lastEditor = null;
        this.editorOptions = {
        };
        this.render()
    },

    events: {
        "click .toggle-hide": "toggleHide",
        "click .toggle-regular": "toggleRegular",
        "click .btn-save": "save",
        "click input": "stop",
        "click .m-task .m-task-description": "createTaskItemEditor",
        // "click .m-task .m-task-btn-save": "destroyTaskItemEdit",
        "click .m-lab-description": "createLabEditor",
        "keyup .lab-title-input": "setTitle",
    },

    createTaskItemEditor: function (e) {
        var target = $(e.currentTarget).parents('.m-task')[0];
        if (this.lastEditor && this.lastEditor.view && this.lastEditor.view !== target.view) {
            this.lastEditor.view.removeEditor();
        }
        target.view.createEditor();
        this.lastEditor = target;
    },

    removeLabEditor: function (e) {
        this.$el.find(".m-lab-description").summernote('destroy')
    },

    createLabEditor: function (e) {
        var self = this;
        this.$el.find(".m-lab-description").summernote($.extend(this.editorOptions, {
            callbacks: {
                onChange: function (contents, $editable) {
                    self.model.set('description', contents);
                }
            }
        }));
    },

    save: function (e) {
        var self = this;
        this.model.save().done(function () {
            self.removeLabEditor();
            new Noty({
                theme: 'relax',
                text: "Сохранено",
                type: 'success',
                timeout: 1000
            }).show();
        }).fail(function () {
            new Noty({
                theme: 'relax',
                text: "Ну удалось отсортировать",
                type: 'error',
                timeout: 1000
            }).show();
        });

        e.stopPropagation();
    },

    stop: function (e) {
        e.stopPropagation();
    },

    setTitle: function (e) {
        this.model.set("title", e.currentTarget.value)
    },

    toggleHide: function (e) {
        e.stopPropagation();
        this.model.set('visible', !this.model.get("visible"));
        this.save();
    },

    toggleRegular: function (e) {
        e.stopPropagation();
        this.model.set('regular', !this.model.get("regular"));
        this.save();
    },

    render: function () {
        var is_visible = this.model.get("visible");
        this.$el.find(".toggle-hide ").toggleClass("btn-default", !is_visible);
        this.$el.find(".toggle-hide ").toggleClass("btn-success", is_visible);
        this.$el.find(".toggle-hide .fa").toggleClass("fa-eye-slash", !is_visible);
        this.$el.find(".toggle-hide .fa").toggleClass("fa-eye", is_visible);

        var is_regular = this.model.get("regular");
        this.$el.find(".toggle-regular ").toggleClass("btn-default", !is_regular);
        this.$el.find(".toggle-regular ").toggleClass("btn-success", is_regular);
    }
});