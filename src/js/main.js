import 'vite/modulepreload-polyfill'
import 'nouislider/dist/nouislider.css'
import '../css/main.css'
import '@splidejs/splide/css'
import Splide from '@splidejs/splide'
import htmx from 'htmx.org'
import Alpine from 'alpinejs'
import { initializeApp } from 'firebase/app'
import { getStorage, ref, getDownloadURL } from 'firebase/storage'
import axios from 'axios'
import wNumb from 'wnumb'
import noUiSlider from 'nouislider'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

const config = {
  apiKey: "AIzaSyBZQp1nuuG3ZJeGSuXdaLGPfOFELXEu5kg",
  authDomain: "wbusch-f8fb7.firebaseapp.com",
  databaseURL: "https://wbusch-f8fb7.firebaseio.com",
  projectId: "wbusch-f8fb7",
  storageBucket: "wbusch-f8fb7.appspot.com",
  messagingSenderId: "491905389064",
}
const app = initializeApp(config)
const storage = getStorage()

window.htmx = htmx
window.Alpine = Alpine
window.noUiSlider = noUiSlider

async function getImage(item) {
  const code = item.dataset.code
  const storageRef = ref(storage, `opt/${code}.jpg`)
  try {
    const url = await getDownloadURL(storageRef)
    return url
  } catch (err) {
    return null
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const heroEl = document.querySelector('.hero-splide')
  if (heroEl) {
    const splide = new Splide(heroEl, {
      type: 'loop',
      autoplay: true,
    })
    splide?.mount()
  }
  const slides = document.querySelectorAll('.featured-splide li[data-code]')
  slides.forEach(async s => {
    const url = await getImage(s)
    const img = s.querySelector('img')
    if (url) {
      img.src = url
      img.classList.remove('hidden')
    }
  })

  const featuredEls = document.querySelectorAll('.featured-splide')
  featuredEls.forEach(el => {
    const featuredSplide = new Splide(el, {
      type: 'loop',
      perPage: 4,
      gap: '.25rem',
      breakpoints: {
        640: {
          perPage: 1,
        },
        1023: {
          perPage: 2,
        },
        1279: {
          perPage: 3,
        },
      },
    })
    featuredSplide?.mount()
  })
})

function loadMissingImages(target) {
  const items = target.querySelectorAll('[data-code].hidden')
  items.forEach(async item => {
    const url = await getImage(item)
    if (url) {
      item.src = url
      item.classList.remove('hidden')
    }
  })
}

htmx.onLoad(function (target) {
  loadMissingImages(target)
})

Alpine.data('yearData', () => ({
  open: true,
  originalMin: null,
  originalMax: null,
  init() {
    const yearMin = JSON.parse(document.querySelector('#year-min').textContent)
    const yearMax = JSON.parse(document.querySelector('#year-max').textContent)
    this.originalMin = yearMin
    this.originalMax = yearMax
    noUiSlider.create(
      this.$refs.range,
      {
        format: wNumb({
          decimals: 0
        }),
        step: 1,
        tooltips: true,
        connect: true,
        range: {
          min: yearMin,
          max: yearMax,
        },
        start: [yearMin, yearMax],
      }
    )
    this.$refs.range.noUiSlider.on('end', (values) => {
      const [min, max] = values
      const event = new CustomEvent('filter:year', { detail: { min: Number(min), max: Number(max) } })
      document.dispatchEvent(event)
    })
    document.addEventListener('filter:clear', () => {
      this.$refs.range.noUiSlider.set([this.originalMin, this.originalMax])
    })
  }
}))

Alpine.data('lineData', () => ({
  open: true,
  originalLines: [],
  lines: [],
  selectedLines: [],
  query: '',
  init() {
    const b = JSON.parse(document.querySelector('#lines').textContent)
    this.lines = b
    this.originalLines = b
    document.addEventListener('filter:clear', () => {
      this.selectedLines = []
    })
  },
  dispatch() {
    const event = new CustomEvent('filter:lines', { detail: { lines: this.selectedLines } })
    document.dispatchEvent(event)
  },
}))

Alpine.data('brandData', () => ({
  open: true,
  originalBrands: [],
  brands: [],
  selectedBrands: [],
  query: '',
  init() {
    const b = JSON.parse(document.querySelector('#brands').textContent)
    this.brands = b
    this.originalBrands = b
    document.addEventListener('filter:clear', () => {
      this.selectedBrands = []
    })
  },
  dispatch() {
    const event = new CustomEvent('filter:brands', { detail: { brands: this.selectedBrands } })
    document.dispatchEvent(event)
  },
  async search() {
    if (this.query.length > 2) {
      const res = await axios.get('/productos/marcas/', { params: { nombre__icontains: this.query } })
      this.brands = res.data.results
    } else {
      this.brands = this.originalBrands
    }
  }
}))

Alpine.data('modelData', () => ({
  open: true,
  originalModels: [],
  models: [],
  selectedModels: [],
  query: '',
  init() {
    const m = JSON.parse(document.querySelector('#models').textContent)
    this.models = m
    this.originalModels = m
    document.addEventListener('filter:clear', () => {
      this.selectedModels = []
    })
  },
  dispatch() {
    const event = new CustomEvent('filter:models', { detail: { models: this.selectedModels } })
    document.dispatchEvent(event)
  },
  async search() {
    if (this.query.length > 2) {
      const res = await axios.get('/productos/modelos/', { params: { nombre__icontains: this.query } })
      console.log(res.data.results)
      this.models = res.data.results
    } else {
      this.models = this.originalModels
    }
  },
}))

Alpine.data('fullCartData', () => ({
  cart: null,
  text: '',
  init() {
    this.$watch('cart', v => {
      this.encodeCart()
    })
    const cartStorage = localStorage.getItem('cart');
    if (cartStorage) {
      this.cart = JSON.parse(cartStorage)
    }
  },
  get total() {
    return Object.values(this.cart).map(item => item.count).reduce((a, v) => a + v)
  },
  get totalFormatted() {
    return `(${this.total} items)`
  },
  encodeCart() {
    if (!this.cart) {
      this.text = ''
      return
    }
    const items = Object.values(this.cart).map((v, i) => {
      return `${i + 1}. ${v.code} cantidad: ${v.count}`
    }).join('\n')
    this.text = encodeURIComponent(`Solicito cotización de:\n${items}`)
  },
  increase(code) {
    this.cart[code].count += 1
    const event = new CustomEvent('cart:update', { detail: { code, count: 1, desc: '' } })
    document.dispatchEvent(event)
  },
  decrease(code) {
    this.cart[code].count -= 1
    const event = new CustomEvent('cart:update', { detail: { code, count: -1, desc: '' } })
    document.dispatchEvent(event)
  },
  remove(code) {
    delete this.cart[code]
    const event = new CustomEvent('cart:remove', { detail: { code } })
    document.dispatchEvent(event)
  }
}))

Alpine.data('cart', () => ({
  cart: {},
  total: 0,
  init() {
    let cartStorage = localStorage.getItem('cart')
    if (cartStorage) {
      this.cart = JSON.parse(cartStorage)
      this.total = this.getTotal()
    }
  },
  update(e) {
    const code = e.detail.code
    const desc = e.detail.desc
    if (!this.cart[code]) {
      this.cart[code] = { code, count: 0, desc, }
    }
    this.cart[code].count += e.detail.count
    this.total = this.getTotal()
    const cartStorage = JSON.stringify(this.cart)
    localStorage.setItem('cart', cartStorage)
  },
  remove(e) {
    const code = e.detail.code
    delete this.cart[code]
    this.total = this.getTotal()
    const cartStorage = JSON.stringify(this.cart)
    localStorage.setItem('cart', cartStorage)
  },
  getTotal() {
    if (!this.cart || !Object.keys(this.cart).length) return 0
    return Object.values(this.cart).map(item => item.count).reduce((a, v) => a + v)
  }
}))

Alpine.data('product', () => ({
  count: 1,
  addToCart(e) {
    const form = e.target
    const code = form.code.value
    const desc = form.desc.value
    const count = Number(form.count.value)
    const event = new CustomEvent('cart:update', { detail: { code, count: count, desc, } })
    document.dispatchEvent(event)
  }
}))

Alpine.data('products', () => ({
  previous: null,
  next: null,
  count: null,
  pages: null,
  showEnd: false,
  productos: [],
  params: {},
  observer: null,
  target: document.querySelector('body'),
  addToCart(e) {
    const form = e.target
    const code = form.code.value
    const desc = form.desc.value
    const count = Number(form.count.value)
    const event = new CustomEvent('cart:update', { detail: { code, count: count, desc, } })
    document.dispatchEvent(event)
  },
  handleFilter() {
    const event = new CustomEvent('filter:open')
    document.dispatchEvent(event)
    const body = document.querySelector('body')
    body.classList.add('overflow-hidden')
  },
  async reset() {
    const resetStartEvent = new CustomEvent('reset:start')
    const resetEndEvent = new CustomEvent('reset:end')
    document.dispatchEvent(resetStartEvent)
    this.disconnect()
    this.productos = []
    const res = await axios.get('/productos/productos/', { params: this.params })
    this.productos = res.data.results
    this.next = res.data.next
    this.$nextTick(() => {
      loadMissingImages(this.target)
      this.observe()
      document.dispatchEvent(resetEndEvent)
    })
  },
  observe() {
    if (!this.$refs.next) return
    const options = {
      root: null,
      threshold: 0.1
    }
    this.observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          if (this.next) {
            axios.get(this.next, { params: this.params })
              .then(res => {
                this.productos.push(...res.data.results)
                this.next = res.data.next
                loadMissingImages(this.target)
              })
          }
        }
      })
    }, options)
    this.observer.observe(this.$refs.next)
  },
  disconnect() {
    if (this.observer) {
      this.observer.disconnect()
    }
  },
  init() {
    this.params = JSON.parse(document.querySelector('#filters').textContent)
    this.productos = JSON.parse(document.querySelector('#products').textContent)
    this.next = JSON.parse(document.querySelector('#next').textContent)
    this.pages = Math.ceil(this.count / 10)
    this.observe()
    document.addEventListener('filter:year', async e => {
      const { min, max } = e.detail
      this.params['producto_modelos__ano__range'] = `${min},${max}`
      this.reset()
    })
    document.addEventListener('filter:lines', e => {
      const { lines } = e.detail
      this.params['tipo__in'] = lines.join(',')
      this.reset()
    })
    document.addEventListener('filter:brands', e => {
      const { brands } = e.detail
      this.params['producto_modelos__modelo__marca__in'] = brands.join(',')
      this.reset()
    })
    document.addEventListener('filter:models', e => {
      const { models } = e.detail
      this.params['producto_modelos__modelo__in'] = models.join(',')
      this.reset()
    })
  },
  clearFilters() {
    this.params = {}
    this.reset()
    const event = new CustomEvent('filter:clear')
    document.dispatchEvent(event)
  },
}))
Alpine.data('contact', () => ({
  sent: false,
  success: false,
  sendEmail(e) {
  const form = e.target;
  const formData = new FormData(form);
  axios.post(form.action, formData)
  .then(response => {
    console.log(response)
    this.sent = true;
    this.success = response.data.success;
  })
  .catch(error => {
    console.log(error)
    this.sent = true;
    this.success = false;
  })
}
}))
Alpine.start()

const imgContainers = document.querySelectorAll('.image-container')

imgContainers.forEach(container => {
  const img = container.querySelector('img')
  container.addEventListener('mousemove', (e) => {
    const { left, top, width, height } = container.getBoundingClientRect();
    const x = (e.clientX - left) / width * 100
    const y = (e.clientY - top) / height * 100
    img.style.transformOrigin = `${x}% ${y}%`
    img.style.transform = 'scale(2)'
  })

  container.addEventListener('mouseleave', () => {
    img.style.transform = 'scale(1)'
    img.style.transformOrigin = 'center'
  })
})