use crate::{
    sv_misc::{get_string, identifier},
    sv_net_type::SvNetType,
    sv_packed_dimension::SvPackedDimension,
    sv_port_direction::SvPortDirection,
    sv_unpacked_dimension::SvUnpackedDimension,
};
use pyo3::prelude::*;
use std::fmt;
use sv_parser::{unwrap_node, RefNode, SyntaxTree};
#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SvPort {
    #[pyo3(get, set)]
    pub identifier: String,
    #[pyo3(get, set)]
    pub direction: SvPortDirection,
    #[pyo3(get, set)]
    pub net_type: Option<SvNetType>,
    #[pyo3(get, set)]
    pub packed_dimensions: Vec<SvPackedDimension>,
    #[pyo3(get, set)]
    pub unpacked_dimensions: Vec<SvUnpackedDimension>,
}

#[pymethods]
impl SvPort {
    #[pyo3(signature = (identifier, direction, packed_dimensions, unpacked_dimensions, net_type=None))]
    #[new]
    fn new(
        identifier: String,
        direction: SvPortDirection,
        packed_dimensions: Vec<SvPackedDimension>,
        unpacked_dimensions: Vec<SvUnpackedDimension>,
        net_type: Option<SvNetType>,
    ) -> Self {
        SvPort {
            identifier,
            direction,
            packed_dimensions,
            unpacked_dimensions,
            net_type,
        }
    }

    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvPort {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.direction)?;

        if self.net_type.is_none() {
            write!(f, " var logic ")?;
        } else {
            write!(f, " tri logic ")?;
        }

        for packed_dimension in &self.packed_dimensions {
            write!(f, "{}", packed_dimension)?;
        }

        if self.packed_dimensions.is_empty() {
            write!(f, "{}", self.identifier)?;
        } else {
            write!(f, " {}", self.identifier)?;
        }

        for unpacked_dimension in &self.unpacked_dimensions {
            write!(f, "{}", unpacked_dimension)?;
        }

        Ok(())
    }
}

pub fn port_declaration_ansi(
    p: &sv_parser::AnsiPortDeclaration,
    syntax_tree: &SyntaxTree,
    previous_port: &Option<SvPort>,
) -> SvPort {
    let inherit = port_check_inheritance_ansi(p, previous_port);

    if inherit {
        let previous_port = previous_port.clone().unwrap();
        SvPort {
            identifier: port_identifier(p, syntax_tree),
            direction: previous_port.direction,
            net_type: previous_port.net_type,
            packed_dimensions: previous_port.packed_dimensions,
            unpacked_dimensions: port_unpacked_dimension_ansi(
                RefNode::AnsiPortDeclaration(p),
                syntax_tree,
            ),
        }
    } else {
        SvPort {
            identifier: port_identifier(p, syntax_tree),
            direction: port_direction_ansi(p, previous_port),
            packed_dimensions: port_packed_dimension_ansi(
                RefNode::AnsiPortDeclaration(p),
                syntax_tree,
            ),
            net_type: port_net_type_ansi(p, &port_direction_ansi(p, previous_port)),
            unpacked_dimensions: port_unpacked_dimension_ansi(
                RefNode::AnsiPortDeclaration(p),
                syntax_tree,
            ),
        }
    }
}

fn port_identifier(node: &sv_parser::AnsiPortDeclaration, syntax_tree: &SyntaxTree) -> String {
    if let Some(id) = unwrap_node!(node, PortIdentifier) {
        identifier(id, syntax_tree).unwrap()
    } else {
        unreachable!()
    }
}

fn port_direction_ansi(
    node: &sv_parser::AnsiPortDeclaration,
    previous_port: &Option<SvPort>,
) -> SvPortDirection {
    let dir = unwrap_node!(node, PortDirection);
    match dir {
        Some(RefNode::PortDirection(sv_parser::PortDirection::Inout(_))) => SvPortDirection::Inout,
        Some(RefNode::PortDirection(sv_parser::PortDirection::Input(_))) => SvPortDirection::Input,
        Some(RefNode::PortDirection(sv_parser::PortDirection::Output(_))) => {
            SvPortDirection::Output
        }
        Some(RefNode::PortDirection(sv_parser::PortDirection::Ref(_))) => SvPortDirection::Ref,
        _ => match previous_port {
            Some(_) => previous_port.clone().unwrap().direction,
            None => SvPortDirection::Inout,
        },
    }
}
pub fn port_packed_dimension_ansi(m: RefNode, syntax_tree: &SyntaxTree) -> Vec<SvPackedDimension> {
    let mut ret: Vec<SvPackedDimension> = Vec::new();

    for node in m {
        if let RefNode::PackedDimensionRange(x) = node {
            let range = unwrap_node!(x, ConstantRange);
            if let Some(RefNode::ConstantRange(sv_parser::ConstantRange { nodes })) = range {
                let (l, _, r) = nodes;
                let left_bound = get_string(RefNode::ConstantExpression(l), syntax_tree).unwrap();
                let right_bound = get_string(RefNode::ConstantExpression(r), syntax_tree).unwrap();

                ret.push(SvPackedDimension {
                    left_bound,
                    right_bound,
                });
            }
        }
    }

    ret
}

pub fn port_unpacked_dimension_ansi(
    m: RefNode,
    syntax_tree: &SyntaxTree,
) -> Vec<SvUnpackedDimension> {
    let mut ret: Vec<SvUnpackedDimension> = Vec::new();

    for node in m {
        match node {
            RefNode::UnpackedDimensionRange(x) => {
                let range = unwrap_node!(x, ConstantRange);
                if let Some(RefNode::ConstantRange(sv_parser::ConstantRange { nodes })) = range {
                    let (l, _, r) = nodes;
                    let left_bound =
                        get_string(RefNode::ConstantExpression(l), syntax_tree).unwrap();
                    let right_bound =
                        get_string(RefNode::ConstantExpression(r), syntax_tree).unwrap();

                    ret.push(SvUnpackedDimension {
                        left_bound,
                        right_bound: Some(right_bound),
                    });
                }
            }
            RefNode::UnpackedDimensionExpression(x) => {
                let range = unwrap_node!(x, ConstantExpression).unwrap();
                let left_bound = get_string(range, syntax_tree).unwrap();

                ret.push(SvUnpackedDimension {
                    left_bound,
                    right_bound: None,
                });
            }
            _ => (),
        }
    }

    ret
}
fn port_net_type_ansi(
    m: &sv_parser::AnsiPortDeclaration,
    direction: &SvPortDirection,
) -> Option<SvNetType> {
    let objecttype = unwrap_node!(m, AnsiPortDeclarationVariable, AnsiPortDeclarationNet);
    match objecttype {
        Some(RefNode::AnsiPortDeclarationVariable(_)) => {
            match unwrap_node!(m, PortDirection, DataType, Signing, PackedDimension) {
                Some(_) => None,
                _ => Some(SvNetType::Wire),
            }
        }

        Some(RefNode::AnsiPortDeclarationNet(x)) => {
            let nettype = unwrap_node!(x, NetType);

            match nettype {
                // "Var" token was not found
                Some(RefNode::NetType(sv_parser::NetType::Supply0(_))) => Some(SvNetType::Supply0),
                Some(RefNode::NetType(sv_parser::NetType::Supply1(_))) => Some(SvNetType::Supply1),
                Some(RefNode::NetType(sv_parser::NetType::Triand(_))) => Some(SvNetType::Triand),
                Some(RefNode::NetType(sv_parser::NetType::Trior(_))) => Some(SvNetType::Trior),
                Some(RefNode::NetType(sv_parser::NetType::Trireg(_))) => Some(SvNetType::Trireg),
                Some(RefNode::NetType(sv_parser::NetType::Tri0(_))) => Some(SvNetType::Tri0),
                Some(RefNode::NetType(sv_parser::NetType::Tri1(_))) => Some(SvNetType::Tri1),
                Some(RefNode::NetType(sv_parser::NetType::Tri(_))) => Some(SvNetType::Tri),
                Some(RefNode::NetType(sv_parser::NetType::Uwire(_))) => Some(SvNetType::Uwire),
                Some(RefNode::NetType(sv_parser::NetType::Wire(_))) => Some(SvNetType::Wire),
                Some(RefNode::NetType(sv_parser::NetType::Wand(_))) => Some(SvNetType::Wand),
                Some(RefNode::NetType(sv_parser::NetType::Wor(_))) => Some(SvNetType::Wor),

                _ => match direction {
                    SvPortDirection::Inout | SvPortDirection::Input => Some(SvNetType::Wire),
                    SvPortDirection::Output => match unwrap_node!(m, DataType) {
                        Some(_) => None,
                        _ => Some(SvNetType::Wire),
                    },

                    SvPortDirection::Ref => None,

                    _ => unreachable!(),
                },
            }
        }

        _ => unreachable!(),
    }
}

fn port_check_inheritance_ansi(
    m: &sv_parser::AnsiPortDeclaration,
    previous_port: &Option<SvPort>,
) -> bool {
    let datatype = unwrap_node!(
        m,
        DataType,
        Signing,
        NetType,
        VarDataType,
        PortDirection,
        PackedDimension
    );

    match previous_port {
        Some(_) => datatype.is_none(),
        None => false,
    }
}
