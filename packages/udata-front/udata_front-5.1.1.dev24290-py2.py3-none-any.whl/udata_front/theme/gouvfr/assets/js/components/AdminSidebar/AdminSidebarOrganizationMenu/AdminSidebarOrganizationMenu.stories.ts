import type { Meta, StoryObj } from "@storybook/vue3";
import AdminSidebarOrganizationMenu from "./AdminSidebarOrganizationMenu.vue";
import type { Organization } from "@datagouv/components";

const meta = {
  title: "Admin/AdminSidebarOrganizationMenu",
  component: AdminSidebarOrganizationMenu,
} satisfies Meta<typeof AdminSidebarOrganizationMenu>;

export default meta;

const organization : Organization = {
  id: "someId",
  acronym: null,
  name: "data.gouv.fr",
  badges: [],
  page: "https://www.data.gouv.fr/fr/organizations/data-gouv-fr/",
  uri: "https://www.data.gouv.fr/fr/organizations/data-gouv-fr/",
  slug: "data-gouv-fr",
  logo: "https://static.data.gouv.fr/avatars/09/1ba932cbfa48dc8c158981de6c700a.jpeg",
  logo_thumbnail: "https://static.data.gouv.fr/avatars/09/1ba932cbfa48dc8c158981de6c700a-100.jpeg",
};

export const Opened: StoryObj<typeof meta> = {
  render: (args) => ({
    components: { AdminSidebarOrganizationMenu },
    setup() {
      return { args };
    },
    template: `<ul class="fr-sidemenu"><AdminSidebarOrganizationMenu v-bind="args"/></ul>`,
  }),
  args: {
    organization,
    isOpened: true,
  },
};

export const Closed: StoryObj<typeof meta> = {
  render: (args) => ({
    components: { AdminSidebarOrganizationMenu },
    setup() {
      return { args };
    },
    template: `<ul class="fr-sidemenu"><AdminSidebarOrganizationMenu v-bind="args"/></ul>`,
  }),
  args: {
    organization,
    isOpened: false,
  },
};
