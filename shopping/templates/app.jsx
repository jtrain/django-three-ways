// our list of lists.
//

class AllLists extends React.Component {

    constructor(props) {
        super(props);
        this.state = {search: ''}
    }


    render() {
        const lis = this.props.lists.map(ShoppingList);
        return (
          <div>
            <div className='filters'>
                <form onSubmit={
                    (e) => {
                        e.preventDefault();
                        this.props.doSearch(this.state.search)
                    }
                }>
                    <input
                        onChange={
                            (e) => this.setState({search: e.target.value})
                        }
                        value={this.state.search}
                        placeholder='Search' />
                </form>
            </div>
            <table>
                <thead>
                  <tr>
                    <th><a href="/?ordering=lower_name">Name</a></th>
                    <th><a href="/?ordering=-item_count">Products</a></th>
                    <th><a href="/?ordering=-created_at">Created</a></th>
                  </tr>
                </thead>
                <tbody>{lis}</tbody>
            </table>
          </div>
        );
    }
}

class ProductForm extends React.Component {

    render() {
        return (
            <div key={this.props.id}>
                <legend>Product {this.props.id + 1} {this.props.name}-{this.props.quantity}</legend>
                <div className="form-group">
                    <label>Name</label>
                    <input className="form-control"
                        onChange={(event) => this.props.onChange(
                                    this.props.id, 'name', event.target.value)}
                        id={this.props.id + '-name'}
                        placeholder="Product Name" />
                </div>
                <div className="form-group">
                    <label>Quantity</label>
                    <input type="number" className="form-control"
                        onChange={(event) => this.props.onChange(
                                    this.props.id, 'quantity', event.target.value)}
                        id={this.props.id + '-quantity'} placeholder="0" />
                </div>
            </div>
        );
    }
}

class CreateListForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {name: null, items: [{name: null, quantity: null}]};
        this.handleChangeEvent = this.handleChangeEvent.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddProduct = this.handleAddProduct.bind(this);
        this.handleProductChange = this.handleProductChange.bind(this);
    }

    handleChangeEvent (event) {
        this.setState({name: event.target.value})
    }

    handleSubmit (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: '/api/v1/lists/',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(this.state),
            dataType: 'json',
            success: (data) => doRoute(data.url, true)
        });
    }

    handleAddProduct (event) {
        event.preventDefault();
        this.setState({items: this.state.items.concat([{name: null, quantity: null}])});
    }

    handleProductChange (id, attr, value) {
        let items = this.state.items.concat([]);
        items[id][attr] = value;
        this.setState({items: items});
    }

    render() {
      const products = this.state.items.map((product, id) =>
            <ProductForm id={id} onChange={this.handleProductChange}
                        name={product.name} quantity={product.quantity} />
      );

      return (
        <form>
            <legend>Shopping List {this.state.name}</legend>
            <div className="form-group">
                <label>Name</label>
                <input type="text" className="form-control"
                    onChange={this.handleChangeEvent}
                    id="name" placeholder="Name" />
            </div>

            {products}

            <button className="btn btn-default" onClick={this.handleAddProduct}>Add Product</button>
            <button className="btn btn-default" onClick={this.handleSubmit}>Create List</button>
        </form>
      );
    }
}

function DetailProduct(props) {
    return (
      <tr>
        <td>{props.name}</td>
        <td>{props.quantity}</td>
      </tr>
    );
}

function DetailList(props) {
    const list = props.list;
    const products = list.items.map(DetailProduct);
    return (
        <div>
            <h1>{list.name}</h1>
            <table>
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                  </tr>
                </thead>
                <tbody>{products}</tbody>
            </table>
        </div>
    );
}

function ShoppingList(props) {
    return (
        <tr key={props.url}>
            <td><a href={props.url}>{props.name}</a></td>
            <td>{props.items.length}</td>
            <td>{moment(props.created_at).fromNow()}</td>
        </tr>
    );
}

window.onpopstate = function (event) {
    doRoute(event.target.location.pathname);
}

window.onload = function (event) {
    doRoute(event.target.location.pathname);
}

$(document).on('click', 'a', function(event) {
    event.preventDefault();
    const href = $(event.target).attr('href');
    doRoute(href, true);
});

function doRoute(url, push) {
    if (push === true) {
        history.pushState({}, '', url);
    }
    let a = document.createElement('a');
    a.href = url;
    let resolved = resolve(a.pathname);
    resolved.route.init(resolved, a);
}

function listsPage(routeMatch, request) {
    $.get('/api/v1/lists/' + request.search, function(data) {
        ReactDOM.render(
            <AllLists lists={data} doSearch={
                (q) => doRoute('/?search=' + q, true)
            } />,
            document.getElementById('root')
        )
    });
}

function listsCreatePage(routeMatch) {
    ReactDOM.render(
        <CreateListForm />,
        document.getElementById('root')
    );
}

function listsDetailPage(routeMatch) {
    $.get('/api/v1/lists/' + routeMatch.match[1] + '/', function(data) {
        ReactDOM.render(
            <DetailList list={data} />,
            document.getElementById('root')
        )
    });

}

window.routes = [
    {url: '^/$', init: listsPage},
    {url: '^/lists/create/$', init: listsCreatePage},
    {url: '^/lists/(\\d+)/$', init: listsDetailPage}
];

function isMatch(url, route) {
    return url.match(route.url);
}

function resolve(url) {
    for (const route of routes) {
        let match = url.match(route.url);
        if (match !== null) {
            return {
                url: url,
                route: route,
                match: match
            }
        };
    }
    return undefined;
}
