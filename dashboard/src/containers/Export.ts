import { connect } from 'react-redux';

import { RootState } from '../types';
import { ExportFilters } from '../api/types'
import Export, { Props } from '../components/Export';
import * as dispatchers from '../dispatchers';

function mapStateToProps(state: RootState): Props {
	return {
		filters: state.filters,
	};
}

const mapDispatchToProps = (dispatch: any) => ({
	downloadCSV: (filters: ExportFilters) => dispatch(dispatchers.downloadCSV(filters)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Export);
