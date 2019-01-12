"""PytSite Content Menu Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import menu as _menu, form as _form, odm as _odm, content as _content


class ContentMenu(_menu.Menu):
    @property
    def entity(self) -> _content.ContentWithURL:
        return self.f_get('entity')

    @entity.setter
    def entity(self, value: _content.ContentWithURL):
        self.f_set('entity', value)

    def _setup_fields(self):
        super()._setup_fields()

        self.remove_field('title')
        self.remove_field('path')

        self.define_field(_odm.field.Ref('entity', required=True, model_cls=_content.ContentWithURL))
        self.define_field(_odm.field.Virtual('title'))
        self.define_field(_odm.field.Virtual('path'))

    def _on_f_get(self, field_name: str, value, **kwargs):
        if field_name in ('title', 'path') and self.entity:
            if field_name == 'title':
                return self.entity.title
            if field_name == 'path':
                return self.entity.route_alias.alias

        return super()._on_f_get(field_name, value)

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        for uid in ('_parent', 'path', 'title'):
            if frm.has_widget(uid):
                frm.remove_widget(uid)

        frm.add_widget(_content.widget.EntitySelect(
            uid='entity',
            weight=150,
            label=self.t('content'),
            required=self.get_field('entity').required,
            value=self.entity,
        ))
