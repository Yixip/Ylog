module.exports = {
	title: '我的博客',
	description: '记录与分享',
	theme: 'reco',
	locales: { '/': { lang: 'zh-CN' } },
	themeConfig: {
		type: 'blog',
		author: '你的名字',
		nav: [
			{ text: '首页', link: '/' },
			{ text: '归档', link: '/timeline/', icon: 'reco-date' }
		],
		blogConfig: {
			category: { location: 2, text: '分类' },
			tag: { location: 3, text: '标签' }
		},
		sidebar: 'auto',
		lastUpdated: '上次更新'
	},
	head: [
		['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1' }]
	],
	plugins: [
		'fulltext-search',
		['sitemap', { hostname: 'https://yixip.github.io/Ylog' }],
		['feed', { canonical_base: 'https://yixip.github.io/Ylog' }]
	],
	dest: 'docs/.vuepress/dist'
}

