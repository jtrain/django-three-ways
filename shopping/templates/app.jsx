// our list of lists.
//

function AllLists(props) {
    const lists = props.lists;
    const lis = lists.map(ShoppingList);
    return (
        <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Products</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>{lis}</tbody>
        </table>
    );
}

function ShoppingList(props) {
    return (
        <tr>
            <td><a href={props.url}>{props.name}</a></td>
            <td>{props.items.length}</td>
            <td>{moment(props.created_at).fromNow()}</td>
        </tr>
    );
}

$.get('/api/v1/lists/', function(data) {
    ReactDOM.render(
        <AllLists lists={data} />,
        document.getElementById('root')
    )
});
