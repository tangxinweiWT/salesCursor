import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'
import Dashboard from '@/views/Dashboard.vue'
import DataUpload from '@/views/DataUpload.vue'
import DataQuery from '@/views/DataQuery.vue'
import ApiTest from '@/views/ApiTest.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '数据可视化' }
      },
      {
        path: 'upload',
        name: 'DataUpload',
        component: DataUpload,
        meta: { title: '数据上传' }
      },
      {
        path: 'query',
        name: 'DataQuery',
        component: DataQuery,
        meta: { title: '数据查询' }
      },
      {
        path: 'test',
        name: 'ApiTest',
        component: ApiTest,
        meta: { title: 'API测试' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 