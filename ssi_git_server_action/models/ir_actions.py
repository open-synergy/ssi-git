# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    state = fields.Selection(
        selection_add=[("run_git_script", "Run Code On Git Repo")],
        ondelete={"run_git_script": "set default"},
    )
    repo_id = fields.Many2one(
        string="Repository",
        comodel_name="git_repo",
        required=False,
        copy=False,
    )
    branch_id = fields.Many2one(
        string="Branch",
        comodel_name="git_branch",
        domain="[('repo_id', '=', repo_id)]",
        required=False,
        copy=False,
    )
    script_id = fields.Many2one(
        string="Script",
        comodel_name="git_script",
        domain="[('branch_id', '=', branch_id)]",
        required=False,
        copy=False,
    )
    parameter_value_ids = fields.One2many(
        string="Script Parameters",
        comodel_name="git_script.parameter_value",
        inverse_name="server_action_id",
    )

    @api.onchange(
        "script_id",
    )
    def _onchange_script_id(self):
        if self.script_id:
            # Dapatkan parameter_id yang sudah ada
            existing_param_ids = set(self.parameter_value_ids.mapped("parameter_id.id"))

            # Hanya tambahkan parameter yang belum ada
            new_parameters = []
            for param in self.script_id.parameter_ids:
                if param.id not in existing_param_ids:
                    new_parameters.append(
                        (
                            0,
                            0,
                            {
                                "parameter_id": param.id,
                                "value": param.default_value or "",
                            },
                        )
                    )

            # Tambahkan parameter baru ke yang sudah ada
            if new_parameters:
                self.parameter_value_ids = [
                    (4, pv.id) for pv in self.parameter_value_ids
                ] + new_parameters

    def run(self):
        res = super().run()
        for action in self:
            if action.state == "run_git_script" and action.script_id:
                model = self.env[action.model_name]
                active_id = self._context.get("active_id")
                active_ids = self._context.get("active_ids")
                context_env = {
                    "self": self,
                    "model": model,
                    "record": model.browse(active_id),
                    "records": model.browse(active_ids),
                    "context": self._context,
                }
                for param in action.parameter_value_ids:
                    context_env[param.parameter_id.name] = param.parse_value()
                action.script_id._run(context_env)
        return res
