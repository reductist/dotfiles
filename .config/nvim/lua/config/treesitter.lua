local M = {}

function M.setup()
  require("nvim-treesitter.configs").setup {
    -- One of "all", "maintained" (parsers with maintainers), or a list of languages
    ensure_installed = "all",

    -- Install languages synchronously (only applied to `ensure_installed`)
    sync_install = true,

		-- Automatically install missing parsers when entering buffer
		auto_install = true,

    highlight = {
      -- `false` will disable the whole extension
      enable = true,
    },

		-- Incremental selection based on the named nodes from the grammar
		incremental_selection = {
      enable = true,
      keymaps = {
        init_selection = "gnn",
        node_incremental = "grn",
        scope_incremental = "grc",
        node_decremental = "grm",
      },
    },

		textobjects = { enable = true },

		indent = {
			enable = true,
			disable = { "python" },
		},
	}
end

return M
