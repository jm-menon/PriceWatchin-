import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
import './cheapest.css';

const vendors = [
  { id: 'site1', name: 'Vendor 1', label: 'Site1', endpoint: '/products-site-1' },
  { id: 'site2', name: 'Vendor 2', label: 'Site2', endpoint: '/products-site-2' },
  { id: 'site3', name: 'Vendor 3', label: 'Site3', endpoint: '/products-site-3' },
  { id: 'site4', name: 'Vendor 4', label: 'Site4', endpoint: '/products-site-4' },
  { id: 'site5', name: 'Vendor 5', label: 'Site5', endpoint: '/products-site-5' }
];

const menuItems = [
  { key: 'vendors', label: 'Our vendors' },
  { key: 'cheapest', label: 'Search cheapest price' },
  { key: 'history', label: 'Search product history' },
  { key: 'product-vendor', label: 'Search product and vendor' }
];

const hasValidDateRange = (dateFrom, dateTo) => Boolean(dateFrom && dateTo && dateFrom <= dateTo);

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
      {view === 'cheapest' && <CheapestProduct />}
      {view === 'history' && <ProductHistory />}
      {view === 'product-vendor' && <ProductVendorHistory />}
    </main>
  );
}

function Welcome({ onBrowse }) {
  return <section className="welcome page-content">
    <p className="eyebrow">COMPARE SMARTER</p>
    <h1>Find the right price,<br />without the hunt.</h1>
    <p className="intro">Browse, Compare and Shop products from your favourite vendors in one calm, simple, zen place :).</p>
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

function CheapestProduct() {
  const [productId, setProductId] = React.useState('');
  const [dateFrom, setDateFrom] = React.useState('');
  const [dateTo, setDateTo] = React.useState('');
  const [result, setResult] = React.useState(null);
  const [status, setStatus] = React.useState('idle');

  const search = async (event) => {
    event.preventDefault();
    const id = Number(productId);
    if (!Number.isInteger(id) || id < 1 || !hasValidDateRange(dateFrom, dateTo)) {
      setStatus('invalid');
      setResult(null);
      return;
    }

    setStatus('loading');
    setResult(null);
    try {
      const response = await fetch(`/api/tracker/tracker/cheapest_product/${id}/${dateFrom}/${dateTo}`);
      if (!response.ok) throw new Error('Unable to find a price');
      setResult(await response.json());
      setStatus('ready');
    } catch {
      setStatus('error');
    }
  };

  const vendorName = result ? vendors.find((vendor, index) => index + 1 === result.vendor_id)?.name ?? `Vendor ${result.vendor_id}` : '';

  return <section className="page-content cheapest-page">
    <p className="eyebrow">PRICE COMPARISON</p>
    <h1 className="page-title">Find the cheapest price</h1>
    <p className="intro">Enter a product ID and date range to compare prices recorded across all vendors.</p>
    <form className="price-search date-search" onSubmit={search}>
      <label className="search-box"><span aria-hidden="true">⌕</span><input inputMode="numeric" value={productId} onChange={(event) => setProductId(event.target.value)} placeholder="Enter product ID" aria-label="Product ID" /></label>
      <DateRangeInputs dateFrom={dateFrom} dateTo={dateTo} setDateFrom={setDateFrom} setDateTo={setDateTo} />
      <button className="primary-button" type="submit">Find best price</button>
    </form>
    {status === 'loading' && <p className="status">Checking prices…</p>}
    {status === 'invalid' && <p className="status error">Enter a valid product ID and date range. The start date must be before the end date.</p>}
    {status === 'error' && <p className="status error">No price could be found. Make sure the tracker API is running and the product has price data.</p>}
    {status === 'ready' && <section className="cheapest-result" aria-live="polite">
      <span className="result-label">LOWEST CURRENT PRICE</span>
      <strong>₹{Number(result.price).toLocaleString('en-IN')}</strong>
      <p>Available from <b>{vendorName}</b></p>
    </section>}
  </section>;
}

function ProductHistory() {
  const [productId, setProductId] = React.useState('');
  const [dateFrom, setDateFrom] = React.useState('');
  const [dateTo, setDateTo] = React.useState('');
  const [history, setHistory] = React.useState([]);
  const [status, setStatus] = React.useState('idle');

  const search = async (event) => {
    event.preventDefault();
    const id = Number(productId);
    if (!Number.isInteger(id) || id < 1 || !hasValidDateRange(dateFrom, dateTo)) {
      setStatus('invalid');
      setHistory([]);
      return;
    }

    setStatus('loading');
    setHistory([]);
    try {
      const response = await fetch(`/api/tracker/tracker/price_history/${id}/${dateFrom}/${dateTo}`);
      if (!response.ok) throw new Error('Unable to find product history');
      const data = await response.json();
      setHistory([...data].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
      setStatus('ready');
    } catch {
      setStatus('error');
    }
  };

  const vendorName = (vendorId) => vendors.find((vendor, index) => index + 1 === vendorId)?.name ?? `Vendor ${vendorId}`;

  return <section className="page-content history-page">
    <p className="eyebrow">PRICE TIMELINE</p>
    <h1 className="page-title">Search product history</h1>
    <p className="intro">Enter a product ID and date range to review recorded prices across vendors.</p>
    <form className="price-search date-search" onSubmit={search}>
      <label className="search-box"><span aria-hidden="true">⌕</span><input inputMode="numeric" value={productId} onChange={(event) => setProductId(event.target.value)} placeholder="Enter product ID" aria-label="Product ID" /></label>
      <DateRangeInputs dateFrom={dateFrom} dateTo={dateTo} setDateFrom={setDateFrom} setDateTo={setDateTo} />
      <button className="primary-button" type="submit">View history</button>
    </form>
    {status === 'loading' && <p className="status">Loading price history…</p>}
    {status === 'invalid' && <p className="status error">Enter a valid product ID and date range. The start date must be before the end date.</p>}
    {status === 'error' && <p className="status error">No history could be found. Make sure the tracker API is running and the product has price data.</p>}
    {status === 'ready' && <section className="history-results" aria-live="polite">
      <div className="history-heading"><span>PRICE HISTORY</span><small>{history.length} record{history.length === 1 ? '' : 's'}</small></div>
      {!history.length && <p className="status">No prices have been recorded for this product yet.</p>}
      {history.map((record) => <article className="history-row" key={record.price_id}>
        <span className="history-dot" aria-hidden="true"></span>
        <div><strong>{vendorName(record.vendor_id)}</strong><small>{new Date(record.created_at).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</small></div>
        <b>₹{Number(record.price).toLocaleString('en-IN')}</b>
      </article>)}
    </section>}
  </section>;
}

function ProductVendorHistory() {
  const [productId, setProductId] = React.useState('');
  const [vendorId, setVendorId] = React.useState('');
  const [dateFrom, setDateFrom] = React.useState('');
  const [dateTo, setDateTo] = React.useState('');
  const [history, setHistory] = React.useState([]);
  const [status, setStatus] = React.useState('idle');

  const search = async (event) => {
    event.preventDefault();
    const product = Number(productId);
    const vendor = Number(vendorId);
    if (!Number.isInteger(product) || product < 1 || !Number.isInteger(vendor) || vendor < 1 || !hasValidDateRange(dateFrom, dateTo)) {
      setStatus('invalid');
      setHistory([]);
      return;
    }

    setStatus('loading');
    setHistory([]);
    try {
      const response = await fetch(`/api/tracker/tracker/product_vendor_history/${product}/${vendor}/${dateFrom}/${dateTo}`);
      if (!response.ok) throw new Error('Unable to find product vendor history');
      const data = await response.json();
      setHistory([...data].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
      setStatus('ready');
    } catch {
      setStatus('error');
    }
  };

  const selectedVendor = vendors.find((vendor, index) => index + 1 === Number(vendorId));

  return <section className="page-content history-page">
    <p className="eyebrow">VENDOR PRICE TIMELINE</p>
    <h1 className="page-title">Search product and vendor</h1>
    <p className="intro">Choose a vendor, product ID, and date range to review that vendor’s recorded price changes.</p>
    <form className="vendor-history-search" onSubmit={search}>
      <label className="search-box"><span aria-hidden="true">⌕</span><input inputMode="numeric" value={productId} onChange={(event) => setProductId(event.target.value)} placeholder="Enter product ID" aria-label="Product ID" /></label>
      <select className="vendor-select" value={vendorId} onChange={(event) => setVendorId(event.target.value)} aria-label="Vendor">
        <option value="">Choose vendor</option>
        {vendors.map((vendor, index) => <option key={vendor.id} value={index + 1}>{vendor.name} — {vendor.label}</option>)}
      </select>
      <DateRangeInputs dateFrom={dateFrom} dateTo={dateTo} setDateFrom={setDateFrom} setDateTo={setDateTo} />
      <button className="primary-button" type="submit">View history</button>
    </form>
    {status === 'loading' && <p className="status">Loading vendor price history…</p>}
    {status === 'invalid' && <p className="status error">Enter a valid product ID, choose a vendor, and select a valid date range.</p>}
    {status === 'error' && <p className="status error">No history could be found. Make sure the tracker API is running and this vendor has price data for the product.</p>}
    {status === 'ready' && <section className="history-results" aria-live="polite">
      <div className="history-heading"><span>{selectedVendor?.name ?? 'VENDOR'} PRICE HISTORY</span><small>{history.length} record{history.length === 1 ? '' : 's'}</small></div>
      {!history.length && <p className="status">No prices have been recorded for this vendor and product yet.</p>}
      {history.map((record) => <article className="history-row" key={record.price_id}>
        <span className="history-dot" aria-hidden="true"></span>
        <div><strong>{selectedVendor?.name ?? `Vendor ${record.vendor_id}`}</strong><small>{new Date(record.created_at).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</small></div>
        <b>₹{Number(record.price).toLocaleString('en-IN')}</b>
      </article>)}
    </section>}
  </section>;
}

function DateRangeInputs({ dateFrom, dateTo, setDateFrom, setDateTo }) {
  return <div className="date-range">
    <label><span>From</span><input type="date" value={dateFrom} onChange={(event) => setDateFrom(event.target.value)} aria-label="Start date" /></label>
    <label><span>To</span><input type="date" value={dateTo} onChange={(event) => setDateTo(event.target.value)} min={dateFrom || undefined} aria-label="End date" /></label>
  </div>;
}

function ComingSoon({ title }) {
  return <section className="page-content coming-soon"><p className="eyebrow">COMING SOON</p><h1 className="page-title">{title}</h1><p className="intro">This search experience is ready for your next requirements.</p></section>;
}

createRoot(document.getElementById('root')).render(<StrictMode><App /></StrictMode>);
