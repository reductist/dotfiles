local M = {}

_G.dump = function(...)
	print(vim.inspect(...))
end

function M.setup()
	-- Indicate first time installation
	local packer_bootstrap = false

	-- packer.nvim configuration
	local conf = {
		profile = {
			enable = true,
			threshold = 1, -- the amount in ms that a plugins load time must be over for it to be included in the profile
		},

		display = {
			open_fn = function()
				return require("packer.util").float { border = "rounded" }
			end,
		},
	}

	-- Check if packer.nvim is installed
	-- Run PackerCompile if there are changes in this file
	local function packer_init()
		local fn = vim.fn
		local install_path = fn.stdpath "data" .. "/site/pack/packer/start/packer.nvim"
		if fn.empty(fn.glob(install_path)) > 0 then
			packer_bootstrap = fn.system {
				"git",
				"clone",
				"--depth",
				"1",
				"https://github.com/wbthomason/packer.nvim",
				install_path,
			}
			vim.cmd [[packadd packer.nvim]]
		end
		vim.cmd "autocmd BufWritePost plugins.lua source <afile> | PackerCompile"
	end

	-- Plugins
	local function plugins(use)
		use { "wbthomason/packer.nvim" }

		-- Load only when require
		use { "nvim-lua/plenary.nvim", module = "plenary" }

		-- Colorscheme
		use {
			'rose-pine/neovim',
			as = 'rose-pine',
			config = function()
				vim.cmd[[
					colorscheme rose-pine
					hi Normal guibg=NONE
				]]
			end
		}

		use {
			"sainnhe/everforest",
			-- config = function()
			--	vim.cmd "colorscheme everforest"
			-- end,
		}

		use {
			"sainnhe/sonokai",
			config = function()
				vim.cmd [[
					 let g:sonokai_style = 'andromeda'
					 let g:sonokai_better_performance = 1
					 let g:sonokai_enable_italic = 1
					 let g:sonokai_transparent_background = 1
					 let g:sonokai_dim_inactive_windows = 0
					 let g:sonokai_spell_foreground = "colored"
					 let g:sonokai_diagnostic_text_highlight = 1
					 let g:sonokai_diagnostic_line_highlight = 1
					 let g:sonokai_diagnostic_virtual_text = "colored"
					 let g:sonokai_current_word = "italic"
					" colorscheme sonokai
				 ]]
			end,
		}

		use { 
			'olivercederborg/poimandres.nvim',
			config = function()
				require('poimandres').setup {
					bold_vert_split = true, -- use bold vertical separators
					dim_nc_background = true, -- dim 'non-current' window backgrounds
					disable_background = false, -- disable background
					disable_float_background = false, -- disable background for floats
					disable_italics = false, -- disable italics
				}
				vim.cmd[[
					"colorscheme poimandres
					"hi Normal guibg=NONE
				]]
			end
		}

		-- Hyprland syntax
		use {
			"theRealCarneiro/hyprland-vim-syntax",
			requires = { "nvim-treesitter/nvim-treesitter" },
			ft = "hypr",
		}

		-- Startup screen
		use {
			"goolord/alpha-nvim",
			config = function()
				require("config.alpha").setup()
			end,
		}

		-- Git
		use {
			"TimUntersberger/neogit",
			cmd = "Neogit",
			config = function()
				require("config.neogit").setup()
			end,
		}

		-- WhichKey
		use {
			"folke/which-key.nvim",
			event = "VimEnter",
			config = function()
				require("config.whichkey").setup()
			end,
		}

		-- IndentLine
		use {
			"lukas-reineke/indent-blankline.nvim",
			event = "BufReadPre",
			config = function()
				require("config.indentblankline").setup()
			end,
		}

		-- Better icons
		use {
			"kyazdani42/nvim-web-devicons",
			module = "nvim-web-devicons",
			config = function()
				require("nvim-web-devicons").setup { default = true }
			end,
		}

		-- Better Comment
		use {
			"numToStr/Comment.nvim",
			keys = { "gc", "gcc", "gbc" },
			config = function()
				require("Comment").setup {}
			end,
		}

		-- Easy hopping
		use {
			"phaazon/hop.nvim",
			cmd = { "HopWord", "HopChar1" },
			config = function()
				require("hop").setup {}
			end,
			disable = true,
		}

		-- Easy motion
		use {
			"ggandor/lightspeed.nvim",
			keys = { "s", "S", "f", "F", "t", "T" },
			config = function()
				require("lightspeed").setup {}
			end,
		}

		-- Better Netrw
		use {"tpope/vim-vinegar"}

		-- Markdown
		use {
			"iamcco/markdown-preview.nvim",
			run = function()
				vim.fn["mkdp#util#install"]()
			end,
			ft = "markdown",
			cmd = { "MarkdownPreview" },
		}

		-- Status line
		use {
			"nvim-lualine/lualine.nvim",
			event = "VimEnter",
			config = function()
				require("config.lualine").setup()
			end,
			requires = { "nvim-web-devicons" },
		}

		-- Treesitter
		use {
			"nvim-treesitter/nvim-treesitter",
			run = ":TSUpdate",
			config = function()
				require("config.treesitter").setup()
			end,
		}

		use {
			"SmiteshP/nvim-gps",
			requires = "nvim-treesitter/nvim-treesitter",
			module = "nvim-gps",
			config = function()
				require("nvim-gps").setup()
			end,
		}

		-- LSP setup
		use { "williamboman/mason.nvim" }
		use { "williamboman/mason-lspconfig.nvim" }
		use { "neovim/nvim-lspconfig" }
		require("mason").setup()
		require("mason-lspconfig").setup({
			ensure_installed = { "rust_analyzer", "tsserver", "pyright"  },
			automatic_installation = true,
		})
		require("mason-lspconfig").setup_handlers({
			function (server_name) -- default handler (optional)
				require("lspconfig")[server_name].setup {}
			end,
		})
		-- Visualize lsp progress
		use({
			"j-hui/fidget.nvim",
			config = function()
				require("fidget").setup()
			end
		})

		-- Autocompletion framework
		use("hrsh7th/nvim-cmp")
		use({
			-- cmp LSP completion
			"hrsh7th/cmp-nvim-lsp",
			-- cmp Snippet completion
			"hrsh7th/cmp-vsnip",
			-- cmp Path completion
			"hrsh7th/cmp-path",
			"hrsh7th/cmp-buffer",
			after = { "hrsh7th/nvim-cmp" },
			requires = { "hrsh7th/nvim-cmp" },
		})
		-- See hrsh7th other plugins for more great completion sources!
		-- Snippet engine
		use('hrsh7th/vim-vsnip')
		-- Adds extra functionality over rust analyzer
		use("simrat39/rust-tools.nvim")

		-- Optional
		use("nvim-lua/popup.nvim")
		use("nvim-telescope/telescope.nvim")

		-- Bootstrap Neovim
		if packer_bootstrap then
			print "Restart Neovim required after installation!"
			require("packer").sync()
		end
	end

	packer_init()

	local packer = require "packer"
	packer.init(conf)
	packer.startup(plugins)
end

return M
