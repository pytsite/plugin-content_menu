"""PytSite Content Menu Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import menu as _menu, form as _form, odm as _odm, content as _content, widget as _widget


class ContentMenu(_menu.Menu):
    @property
    def is_container(self) -> bool:
        return self.f_get('is_container')

    @is_container.setter
    def is_container(self, value: bool):
        self.f_set('is_container', value)

    @property
    def entity(self) -> _content.ContentWithURL:
        return self.f_get('entity')

    @entity.setter
    def entity(self, value: _content.ContentWithURL):
        self.f_set('entity', value)

    def _setup_fields(self):
        super()._setup_fields()

        self.get_field('title').required = False

        self.define_field(_odm.field.Bool('is_container'))
        self.define_field(_odm.field.Ref('entity', model_cls=_content.ContentWithURL))

    def _on_f_get(self, field_name: str, value, **kwargs):
        if field_name in ('title', 'path') and self.entity:
            if field_name == 'title':
                return self.entity.title
            if field_name == 'path':
                return self.entity.route_alias.alias

        return super()._on_f_get(field_name, value)

    def _after_save(self, first_save: bool = False, **kwargs):
        if self.is_container:
            if self.entity:
                self.f_set('entity', None).save()

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        if frm.has_widget('_parent'):
            frm.remove_widget('_parent')

        frm.add_widget(_widget.select.Checkbox(
            uid='is_container',
            weight=25,
            label=self.t('is_container'),
            value=self.is_container,
        ))

        frm.add_widget(_content.widget.EntitySelect(
            uid='entity',
            weight=150,
            label=self.t('content'),
            required=self.get_field('entity').required,
            value=self.entity,
        ))
