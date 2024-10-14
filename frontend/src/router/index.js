import { createWebHistory, createRouter } from 'vue-router'
import SignUp from '../authorization/SignUp.vue'
import MPSSHome from "../views/MPSSHome.vue"
import CreateSection from "../views/CreateSection.vue"
import RequestS from "../views/RequestS.vue"
import BuyBooks from "../views/BuyBooks.vue"
import HomePage from "../views/HomePage.vue"
import ViewBooks from "../views/ViewBooks.vue"
import UserViewBooks from "../views/UserViewBooks.vue"
import CreateBook from "../views/CreateBook.vue"
import EditSection from "../views/EditSection.vue"
import EditBook from "../views/EditBook.vue"
import RequestBook from "../views/RequestBook.vue"
import MyRequests from "../views/MyRequests.vue"
import MyBooks from "../views/MyBooks.vue"
import StatsLib from "../views/StatsLib.vue"
import StatsUser from "../views/StatsUser.vue"
import SearchResults from "../views/SearchResults.vue"
import SearchResultsl from "../views/SearchResultsl.vue"
import ViewDetails from "../views/ViewDetails.vue"
import ViewDetailsLib from "../views/ViewDetailsLib.vue"
import AllBooks from "../views/AllBooks.vue"
import SubScription from "../views/SubScription.vue"
import ABout from "../views/ABout.vue"
import ConTact from "../views/ConTact.vue"
import BuyBook from "../views/BuyBook.vue"

const routes = [
  {
      path: '/register',
      name: 'SignUp',
      component: SignUp
  },
  {
      path: '/',
      name: 'MPSSHome',
      component: MPSSHome
  },
  {
    path: '/createsection',
    name: 'CreateSection',
    component: CreateSection
  },
  {
    path: '/requests',
    name: 'RequestS',
    component: RequestS
  },
  {
    path: '/buybooks',
    name: 'BuyBooks',
    component: BuyBooks
  },
  {
    path: '/myrequests/',
    name: 'MyRequests',
    component: MyRequests
  },
  {
    path: '/mybooks/',
    name: 'MyBooks',
    component: MyBooks
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/section/:id/book',
    name: 'ViewBooks',
    props: true,
    component: ViewBooks
  },
  {
    path: '/section/:id/books',
    name: 'UserViewBooks',
    props: true,
    component: UserViewBooks
  },
  {
    path: '/section/:id/createbook',
    name: 'CreateBook',
    props: true,
    component: CreateBook
  },
  {
    path: '/section/edit/:id/:sec_title/:sec_description',
    name: 'EditSection',
    component: EditSection,
  },
  {
    path: '/book/edit/:id/:book_title/:book_description/:author/',
    name: 'EditBook',
    component: EditBook,
  },
  {
    path: '/requestbook/:id/',
    name: 'RequestBook',
    props: true,
    component: RequestBook
  },
  {
    path: '/buybook/:id/',
    name: 'BuyBook',
    props: true,
    component: BuyBook
  },
  {
    path: '/statslib/',
    name: 'StatsLib',
    component: StatsLib
  },
  {
    path: '/statsuser/',
    name: 'StatsUser',
    component: StatsUser
  },
  {
    path: '/searchresults',
    name: 'SearchResults',
    component: SearchResults
  },
  {
    path: '/searchresultsl',
    name: 'SearchResultsl',
    component: SearchResultsl
  },
  {
    path: '/viewdetails/:id',
    name: 'ViewDetails',
    props: true,
    component: ViewDetails
  },
  {
    path: '/viewdetailslib/:id',
    name: 'ViewDetailsLib',
    props: true,
    component: ViewDetailsLib
  },
  {
    path: '/allbooks/',
    name: 'AllBooks',
    component: AllBooks
  },
  {
    path: '/subscription',
    name: 'SubScription',
    component: SubScription
  },
  {
    path: '/about',
    name: 'ABout',
    component: ABout
  },
  {
    path: '/contact',
    name: 'ConTact',
    component: ConTact
  },
  
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
