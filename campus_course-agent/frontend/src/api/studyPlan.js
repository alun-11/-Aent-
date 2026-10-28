import request from '@/utils/request'

export function listStudyPlans(params = {}) {
  return request({
    url: '/api/study-plans', //study-plans 是学习计划的路由
    method: 'get',
    params
  })
}

export function createStudyPlan(content) {
  return request({
    url: '/api/study-plans',
    method: 'post',
    data: { content }
  })
}

export function deleteStudyPlan(id) {
  return request({
    url: `/api/study-plans/${id}`,
    method: 'delete'
  })
}
