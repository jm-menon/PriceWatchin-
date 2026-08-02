import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const vendors = [
  { id: 'site1', name: 'V1', label: 'Site1', endpoint: '/products-site-1' },
  { id: 'site2', name: 'V2', label: 'Site2', endpoint: '/products-site-2' },
  { id: 'site3', name: 'V3', label: 'Site3', endpoint: '/products-site-3' },
  { id: 'site4', name: 'V4', label: 'Site4', endpoint: '/products-site-4' }
];

const menuItems = [
  { key: 'vendors', label: 'Our vendors' },
  { key: 'cheapest', label: 'Search cheapest price' },
  { key: 'history', label: 'Search product history' },
  { key: 'product-vendor', label: 'Search product and vendor' }
];

function App() {
  const [view, setView] = React.useState('welcome');
  const [menuOpen, setMenuOpen] = React.useState(false);
  const [activeVendor, setActiveVendor] = React.useState(null);

  const navigate = (nextView) => {
    setView(nextView);
    setActiveVendor(null);
    setMenuOpen(false);
  };

  const selectVendor = (vendor) => {
    setActiveVendor(vendor);
    setView('vendor');
    setMenuOpen(false);
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => navigate('welcome')} aria-label="Go to welcome page">
          <span className="brand-mark">P</span>
          <span>PriceWatchin</span>
        </button>
        <div className="menu-wrap">
          <button className="menu-button" onClick={() => setMenuOpen((open) => !open)} aria-expanded={menuOpen} aria-label="Open menu">
            <span></span><span></span><span></span>
          </button>
          {menuOpen && (
            <nav className="menu" aria-label="Main navigation">
              {menuItems.map((item) => (
                <button key={item.key} onClick={() => navigate(item.key)}>{item.label}</button>
              ))}
            </nav>
          )}
        </div>
      </header>

      {view === 'welcome' && <Welcome onBrowse={() => navigate('vendors')} />}
      {view === 'vendors' && <VendorList onSelect={selectVendor} />}
      {view === 'vendor' && activeVendor && <VendorProducts vendor={activeVendor} onBack={() => navigate('vendors')} />}
      {['cheapest', 'history', 'product-vendor'].includes(view) && <ComingSoon title={menuItems.find((item) => item.key === view).label} />}
    </main>
  );
}

function Welcome({ onBrowse }) {
  return <section className="welcome page-content">
    <p className="eyebrow">COMPARE SMARTER</p>
    <h1>Find the right price,<br />without the hunt.</h1>
    <p className="intro">Browse products from your favourite vendors in one calm, simple place.</p>
    <button className="primary-button" onClick={onBrowse}>Browse vendors <span aria-hidden="true">→</span></button>
    <div className="hero-orb orb-one"></div><div className="hero-orb orb-two"></div>
  </section>;
}

function VendorList({ onSelect }) {
  return <section className="page-content">
    <p className="eyebrow">OUR VENDORS</p>
    <h1 className="page-title">Choose a store</h1>
    <p className="intro">Open a vendor to view its available products and search its catalogue.</p>
    <div className="vendor-grid">
      {vendors.map((vendor) => <button className="vendor-card" key={vendor.id} onClick={() => onSelect(vendor)}>
        <span className="vendor-avatar">{vendor.name}</span>
        <span className="vendor-copy"><strong>{vendor.name}</strong><small>{vendor.label}</small></span>
        <span className="arrow" aria-hidden="true">→</span>
      </button>)}
    </div>
  </section>;
}

function VendorProducts({ vendor, onBack }) {
  const [products, setProducts] = React.useState([]);
  const [query, setQuery] = React.useState('');
  const [selected, setSelected] = React.useState(null);
  const [status, setStatus] = React.useState('loading');

  React.useEffect(() => {
    let cancelled = false;
    // FastAPI registers the catalogue endpoint with a trailing slash. Calling
    // that canonical URL prevents a redirect to the simulator origin, which
    // would bypass Vite's local proxy and trigger a CORS error.
    fetch(`/api/${vendor.id}${vendor.endpoint}/`)
      .then((response) => { if (!response.ok) throw new Error('Unable to load products'); return response.json(); })
      .then((data) => { if (!cancelled) { setProducts(data); setStatus('ready'); } })
      .catch(() => { if (!cancelled) setStatus('error'); });
    return () => { cancelled = true; };
  }, [vendor]);

  const filtered = products.filter((product) => product.product_name.toLowerCase().includes(query.toLowerCase()));
  const showProduct = (productId) => {
    fetch(`/api/${vendor.id}${vendor.endpoint}/${productId}`)
      .then((response) => { if (!response.ok) throw new Error('Unable to load product'); return response.json(); })
      .then(setSelected)
      .catch(() => setSelected({ error: true }));
  };

  return <section className="page-content products-page">
    <button className="back-button" onClick={onBack}>← All vendors</button>
    <p className="eyebrow">{vendor.label.toUpperCase()}</p>
    <h1 className="page-title">{vendor.name} products</h1>
    <label className="search-box"><span aria-hidden="true">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search products" /></label>
    {status === 'loading' && <p className="status">Loading products…</p>}
    {status === 'error' && <p className="status error">Couldn’t reach {vendor.label}. Start the simulator and try again.</p>}
    {status === 'ready' && <div className="products-list">
      {filtered.map((product) => <button className="product-row" key={product.product_id} onClick={() => showProduct(product.product_id)}>
        <span><strong>{product.product_name}</strong><small>Product #{product.product_id}</small></span><b>₹{Number(product.base_price).toLocaleString('en-IN')}</b>
      </button>)}
      {!filtered.length && <p className="status">No products match “{query}”.</p>}
    </div>}
    {selected && <div className="product-detail" role="status">
      <button aria-label="Close product details" onClick={() => setSelected(null)}>×</button>
      {selected.error ? <p>Couldn’t load this product.</p> : <><small>PRODUCT DETAILS</small><strong>{selected.product_name}</strong><span>₹{Number(selected.base_price).toLocaleString('en-IN')}</span></>}
    </div>}
  </section>;
}

function ComingSoon({ title }) {
  return <section className="page-content coming-soon"><p className="eyebrow">COMING SOON</p><h1 className="page-title">{title}</h1><p className="intro">This search experience is ready for your next requirements.</p></section>;
}

createRoot(document.getElementById('root')).render(<StrictMode><App /></StrictMode>);
