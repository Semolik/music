import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const useGroupsStore = defineStore({
  id: 'groups',
  state: () => ({
    groups: useStorage('groups', []),
  }),
  actions: {
    containsGroup(faculty_id, group_id) {
      return Boolean(this.groups.find(group => {
        return group.faculty_id == faculty_id && group.group_id == group_id;
      }))
    },
    addGroup(faculty_id, group_id, names) {
      this.groups.push({ faculty_id: faculty_id, group_id: group_id, names: names });
    },
    removeGroup(faculty_id, group_id) {
      this.groups = this.groups.filter(group => !(group.faculty_id === faculty_id && group.group_id === group_id));
    }
  }
});
