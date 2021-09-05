<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="10" lg="8" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
          <v-card-title class="justify-center lemon-milk">
            HANDLE USERS
          </v-card-title>
          <v-card-text>
            <users-list :loading="loading" :users="users" @update="getUsers">
              <v-row class="user-row" v-if="page >= pageAmount">
                <v-col cols="12">
                  <v-dialog v-model="addDialog" max-width="30rem" persistent>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        tile
                        icon
                        block
                        color="primary"
                        :loading="loading"
                        v-bind="attrs"
                        v-on="on"
                      >
                        <v-icon>mdi-plus</v-icon>
                      </v-btn>
                    </template>
                    <user-form
                      :user="null"
                      @close="addDialog = false"
                      @update="getUsers"
                    />
                  </v-dialog>
                </v-col>
              </v-row>
              <v-row class="user-row" v-if="pageAmount > 1">
                <v-pagination
                  class="mx-auto pb-4"
                  color="backgroundAlt"
                  v-model="page"
                  :length="pageAmount"
                ></v-pagination>
              </v-row>
            </users-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import type { AxiosRequestConfig } from "axios";
import UsersList from "@/components/UsersList.vue";
import UserForm from "@/components/UserForm.vue";
import User, { UserResponse } from "@/api/User";

@Component({
  components: { UsersList, UserForm },
})
export default class About extends Vue {
  alert = "";
  page = 1;
  total = 0;
  limit = 10;
  users: UserResponse[] = [];
  loading = true;
  addDialog = false;

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  get offset(): number {
    return (this.page - 1) * this.limit;
  }

  get pageAmount(): number {
    return Math.ceil((this.total + 1) / this.limit);
  }

  @Watch("page")
  onPageChange(): void {
    this.getUsers();
  }

  async getUsers(): Promise<void> {
    let config = this.authConfig;

    const response = await User.get_all(
      config,
      this.limit,
      this.offset,
      this.loading
    );

    if (response.data) {
      this.total = response.data.total;
      this.users = response.data.results;
    } else {
      this.alert = response.error ?? "";
    }
    if (response.status === 401) {
      this.$store.commit("logout");
    }

    this.loading = false;
  }

  mounted(): void {
    if (!this.isConnected) {
      this.$router.replace("/");
    } else {
      this.getUsers();
    }
  }
}
</script>
