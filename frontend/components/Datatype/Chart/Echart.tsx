import React, { memo, useEffect, useRef, useState } from 'react';

import * as echarts from 'echarts';
import { EChartsOption } from 'echarts';
import {
  // 直角坐标系内绘图网格组件
  TitleComponentOption, // 提示框组件
  TooltipComponentOption,
} from 'echarts/components';

echarts.registerTheme('wonderland', {
  color: ['#4ea397', '#22c3aa', '#7bd9a5', '#d0648a', '#f58db2', '#f2b3c9'],
  backgroundColor: 'rgba(255,255,255,0)',
  textStyle: {},
  title: {
    textStyle: {
      color: '#666666',
    },
    subtextStyle: {
      color: '#999999',
    },
  },
  line: {
    itemStyle: {
      borderWidth: '2',
    },
    lineStyle: {
      width: '3',
    },
    symbolSize: '8',
    symbol: 'emptyCircle',
    smooth: false,
  },
  radar: {
    itemStyle: {
      borderWidth: '2',
    },
    lineStyle: {
      width: '3',
    },
    symbolSize: '8',
    symbol: 'emptyCircle',
    smooth: false,
  },
  bar: {
    itemStyle: {
      barBorderWidth: 0,
      barBorderColor: '#ccc',
    },
  },
  pie: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  scatter: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  boxplot: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  parallel: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  sankey: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  funnel: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  gauge: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
  },
  candlestick: {
    itemStyle: {
      color: '#d0648a',
      color0: 'transparent',
      borderColor: '#d0648a',
      borderColor0: '#22c3aa',
      borderWidth: '1',
    },
  },
  graph: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc',
    },
    lineStyle: {
      width: '1',
      color: '#cccccc',
    },
    symbolSize: '8',
    symbol: 'emptyCircle',
    smooth: false,
    color: ['#4ea397', '#22c3aa', '#7bd9a5', '#d0648a', '#f58db2', '#f2b3c9'],
    label: {
      color: '#ffffff',
    },
  },
  map: {
    itemStyle: {
      areaColor: '#eeeeee',
      borderColor: '#999999',
      borderWidth: 0.5,
    },
    label: {
      color: '#28544e',
    },
    emphasis: {
      itemStyle: {
        areaColor: 'rgba(34,195,170,0.25)',
        borderColor: '#22c3aa',
        borderWidth: 1,
      },
      label: {
        color: '#349e8e',
      },
    },
  },
  geo: {
    itemStyle: {
      areaColor: '#eeeeee',
      borderColor: '#999999',
      borderWidth: 0.5,
    },
    label: {
      color: '#28544e',
    },
    emphasis: {
      itemStyle: {
        areaColor: 'rgba(34,195,170,0.25)',
        borderColor: '#22c3aa',
        borderWidth: 1,
      },
      label: {
        color: '#349e8e',
      },
    },
  },
  categoryAxis: {
    axisLine: {
      show: true,
      lineStyle: {
        color: '#cccccc',
      },
    },
    axisTick: {
      show: false,
      lineStyle: {
        color: '#333',
      },
    },
    axisLabel: {
      show: true,
      color: '#999999',
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: ['#eeeeee'],
      },
    },
    splitArea: {
      show: false,
      areaStyle: {
        color: ['rgba(250,250,250,0.05)', 'rgba(200,200,200,0.02)'],
      },
    },
  },
  valueAxis: {
    axisLine: {
      show: true,
      lineStyle: {
        color: '#cccccc',
      },
    },
    axisTick: {
      show: false,
      lineStyle: {
        color: '#333',
      },
    },
    axisLabel: {
      show: true,
      color: '#999999',
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: ['#eeeeee'],
      },
    },
    splitArea: {
      show: false,
      areaStyle: {
        color: ['rgba(250,250,250,0.05)', 'rgba(200,200,200,0.02)'],
      },
    },
  },
  logAxis: {
    axisLine: {
      show: true,
      lineStyle: {
        color: '#cccccc',
      },
    },
    axisTick: {
      show: false,
      lineStyle: {
        color: '#333',
      },
    },
    axisLabel: {
      show: true,
      color: '#999999',
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: ['#eeeeee'],
      },
    },
    splitArea: {
      show: false,
      areaStyle: {
        color: ['rgba(250,250,250,0.05)', 'rgba(200,200,200,0.02)'],
      },
    },
  },
  timeAxis: {
    axisLine: {
      show: true,
      lineStyle: {
        color: '#cccccc',
      },
    },
    axisTick: {
      show: false,
      lineStyle: {
        color: '#333',
      },
    },
    axisLabel: {
      show: true,
      color: '#999999',
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: ['#eeeeee'],
      },
    },
    splitArea: {
      show: false,
      areaStyle: {
        color: ['rgba(250,250,250,0.05)', 'rgba(200,200,200,0.02)'],
      },
    },
  },
  toolbox: {
    iconStyle: {
      borderColor: '#999999',
    },
    emphasis: {
      iconStyle: {
        borderColor: '#666666',
      },
    },
  },
  legend: {
    textStyle: {
      color: '#999999',
    },
  },
  tooltip: {
    axisPointer: {
      lineStyle: {
        color: '#cccccc',
        width: 1,
      },
      crossStyle: {
        color: '#cccccc',
        width: 1,
      },
    },
  },
  timeline: {
    lineStyle: {
      color: '#4ea397',
      width: 1,
    },
    itemStyle: {
      color: '#4ea397',
      borderWidth: 1,
    },
    controlStyle: {
      color: '#4ea397',
      borderColor: '#4ea397',
      borderWidth: 0.5,
    },
    checkpointStyle: {
      color: '#4ea397',
      borderColor: '#3cebd2',
    },
    label: {
      color: '#4ea397',
    },
    emphasis: {
      itemStyle: {
        color: '#4ea397',
      },
      controlStyle: {
        color: '#4ea397',
        borderColor: '#4ea397',
        borderWidth: 0.5,
      },
      label: {
        color: '#4ea397',
      },
    },
  },
  visualMap: {
    color: ['#d0648a', '#22c3aa', '#adfff1'],
  },
  dataZoom: {
    backgroundColor: 'rgba(255,255,255,0)',
    dataBackgroundColor: 'rgba(222,222,222,1)',
    fillerColor: 'rgba(114,230,212,0.25)',
    handleColor: '#cccccc',
    handleSize: '100%',
    textStyle: {
      color: '#999999',
    },
  },
  markPoint: {
    label: {
      color: '#ffffff',
    },
    emphasis: {
      label: {
        color: '#ffffff',
      },
    },
  },
});

interface EChartsChartProps {
  content: string;
}

const EChartsChart: React.FC<EChartsChartProps> = memo(({ content }) => {
  const chartRef = useRef<HTMLDivElement>(null);

  const [chartJson, setChartJson] = useState<any>({});

  useEffect(() => {
    const data = JSON.parse(content);
    setChartJson(data);
  }, []);

  useEffect(() => {
    let chartInstance: echarts.ECharts | null = null;

    if (chartRef.current) {
      chartInstance = echarts.init(chartRef.current, 'wonderland');
      if ('color' in chartJson) delete chartJson['color'];
      if ('series' in chartJson) {
        for (let i = 0; i < chartJson['series'].length; ++i) {
          if ('lineStyle' in chartJson['series'][i]) {
            delete chartJson['series'][i]['lineStyle'];
          }
        }
      }
      chartInstance.setOption(chartJson as EChartsOption);
    }
    window.addEventListener('resize', handleResize);
    return () => {
      if (chartInstance) {
        chartInstance.dispose();
      }
      window.removeEventListener('resize', handleResize);
    };
  }, [chartRef.current]);

  const handleResize = () => {
    if (chartRef.current) {
      const chartInstance = echarts.getInstanceByDom(chartRef.current);
      if (chartInstance) {
        chartInstance.resize();
      }
    }
  };

  return <div ref={chartRef} className="w-full h-[500px]" />;
});

export default EChartsChart;
