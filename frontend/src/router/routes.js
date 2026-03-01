const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      //{ path: 'cadastro-perfil', component: () => import('pages/ProfilePage.vue') },
      { path: 'questionario', component: () => import('pages/QuestionarioPage.vue') }
    ]
  },

  // Sempre deixe este por último para capturar erros 404
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
