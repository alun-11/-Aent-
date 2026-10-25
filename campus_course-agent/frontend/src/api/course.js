import request from '@/utils/request'

/**
 * 获取课程列表
 * @param {Object} params - { keywords }
 */
export function listCoursesApi(params) {
  return request({
    url: '/api/courses',
    method: 'get',
    params
  })
}

/**
 * 新增课程
 */
export function createCourseApi(data) {
  return request({
    url: '/api/courses',
    method: 'post',
    data
  })
}

/**
 * 更新课程
 */
export function updateCourseApi(id, data) {
  return request({
    url: `/api/courses/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除课程
 */
export function deleteCourseApi(id) {
  return request({
    url: `/api/courses/${id}`,
    method: 'delete'
  })
}
